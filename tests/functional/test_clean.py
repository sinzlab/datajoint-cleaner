import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import UUID

import datajoint as dj
import docker
import pytest
from dj_cleaner import controller
from minio import Minio

HEALTH_CHECK_MAX_RETRIES = 60
HEALTH_CHECK_INTERVAL = 1

DB_IMAGE_TAG = "8.0.18-slim-827c535"
DB_HOST = "localhost"
DB_USER = "root"
DB_ROOT_PASSWORD = "simple"
DB_PASSWORD = "simple"
DB_PORT = 3306

MINIO_IMAGE_TAG = "RELEASE.2021-01-16T02-19-44Z"
MINIO_ENDPOINT = "localhost"
MINIO_ACCESS_KEY = "access_key"
MINIO_SECRET_KEY = "secret_key"
MINIO_PORT = 9000
MINIO_HEALTHCHECK_START_PERIOD = 0
MINIO_HEALTHCHECK_INTERVAL = 60
MINIO_HEALTHCHECK_RETRIES = 1
MINIO_HEALTHCHECK_TIMEOUT = 5
MINIO_LOCATION = "dj-store"
MINIO_SECURE = "false"

DB_STORE_NAME = "external"
BUCKET_NAME = "my-bucket"
SCHEMA_NAME = "my_schema"


@pytest.fixture
def docker_client():
    return docker.from_env()


@pytest.fixture
def run_container(docker_client):
    class ContainerRunner:
        def __init__(self, container_config):
            self.container_config = container_config
            self.container = None

        def __enter__(self):
            self._run_container()
            self._wait_until_healthy()
            return self.container

        def __exit__(self, type, value, traceback):
            self.container.stop()

        def _run_container(self):
            self.container = docker_client.containers.run(**self.container_config)

        def _wait_until_healthy(self):
            n_tries = 0
            while True:
                self.container.reload()
                if self.container.attrs["State"]["Health"]["Status"] == "healthy":
                    break
                if n_tries >= HEALTH_CHECK_MAX_RETRIES:
                    self.container.stop()
                    raise RuntimeError(
                        f"Container '{self.container.name}' not healthy "
                        f"after max number ({HEALTH_CHECK_MAX_RETRIES}) of retries"
                    )
                time.sleep(HEALTH_CHECK_INTERVAL)
                n_tries += 1

    return ContainerRunner


@pytest.fixture
def run_dj_mysql_container(run_container):
    container_config = {
        "image": "datajoint/mysql:" + DB_IMAGE_TAG,
        "detach": True,
        "auto_remove": True,
        "name": "dj-mysql",
        "environment": {"MYSQL_ROOT_PASSWORD": DB_ROOT_PASSWORD},
        "ports": {DB_PORT: DB_PORT},
    }
    with run_container(container_config):
        yield


@pytest.fixture
def run_minio_container(run_container):
    container_config = {
        "image": "minio/minio:" + MINIO_IMAGE_TAG,
        "command": ["server", "/data"],
        "detach": True,
        "auto_remove": True,
        "name": "minio",
        "environment": {"MINIO_ACCESS_KEY": MINIO_ACCESS_KEY, "MINIO_SECRET_KEY": MINIO_SECRET_KEY},
        "ports": {MINIO_PORT: MINIO_PORT},
        "healthcheck": {
            "test": ["CMD", "curl", "-f", f"{MINIO_ENDPOINT}:{MINIO_PORT}/minio/health/ready"],
            "start_period": int(MINIO_HEALTHCHECK_START_PERIOD * 1e9),
            "interval": int(MINIO_HEALTHCHECK_INTERVAL * 1e9),
            "retries": MINIO_HEALTHCHECK_RETRIES,
            "timeout": int(MINIO_HEALTHCHECK_TIMEOUT * 1e9),
        },
    }
    with run_container(container_config):
        yield


@pytest.fixture
def configure_datajoint():
    dj.config["database.host"] = DB_HOST
    dj.config["database.user"] = DB_USER
    dj.config["database.password"] = DB_ROOT_PASSWORD
    dj.config["stores"] = {
        DB_STORE_NAME: {
            "protocol": "s3",
            "endpoint": f"{MINIO_ENDPOINT}:{MINIO_PORT}",
            "bucket": BUCKET_NAME,
            "location": MINIO_LOCATION,
            "access_key": MINIO_ACCESS_KEY,
            "secret_key": MINIO_SECRET_KEY,
        }
    }


@pytest.fixture
def schema(run_dj_mysql_container, configure_datajoint):
    return dj.schema(SCHEMA_NAME)


@pytest.fixture
def external_table(schema):
    return schema.external[DB_STORE_NAME]


@pytest.fixture
def table(schema):
    @schema
    class Table(dj.Manual):
        definition = f"""
        primary_attr    : int
        ---
        attached_attr   : attach@{DB_STORE_NAME}
        """

    return Table


@pytest.fixture
def minio_client(run_minio_container):
    return Minio(
        endpoint="localhost:" + str(MINIO_PORT), access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False
    )


@pytest.fixture
def make_bucket(minio_client):
    minio_client.make_bucket(BUCKET_NAME)


@pytest.fixture
def temp_dir_name():
    with TemporaryDirectory() as temp_dir_name:
        yield temp_dir_name


@pytest.fixture
def filepaths():
    return []


@pytest.fixture
def insert_entries(temp_dir_name, filepaths, table, make_bucket):
    def _insert_entries(indexes):
        filenames = ["file" + str(i) for i in range(5)]
        filepaths.extend([os.path.join(temp_dir_name, fn) for fn in filenames])
        for filepath in filepaths:
            with open(filepath, "wb") as file:
                file.write(os.urandom(1024))
        table.insert([{"primary_attr": i, "attached_attr": fp} for i, fp in enumerate(filepaths)])

    return _insert_entries


@pytest.fixture
def delete_entries(table, filepaths, external_table):
    def _delete_entries(indexes):
        for i in indexes:
            (table & "primary_attr = " + str(i)).delete_quick()
            del filepaths[i]
        external_table.delete(delete_external_files=False)

    return _delete_entries


@pytest.fixture
def configure_dj_cleaner():
    config_string = f"""
    [database_servers.db_server]
    host = "{DB_HOST}"
    user = "{DB_USER}"
    password = "{DB_PASSWORD}"

    [storage_servers.minio.minio_server]
    endpoint = "{MINIO_ENDPOINT + ":" + str(MINIO_PORT)}"
    access_key = "{MINIO_ACCESS_KEY}"
    secret_key = "{MINIO_SECRET_KEY}"
    secure = {MINIO_SECURE}

    [[cleaning_runs]]
    database_server = "db_server"
    storage_server = "minio.minio_server"
    schema = "{SCHEMA_NAME}"
    store = "{DB_STORE_NAME}"
    bucket = "{BUCKET_NAME}"
    location = "{MINIO_LOCATION}"
    """

    config_file_path = Path("datajoint-cleaner.toml")
    with open(config_file_path, "w") as config_file:
        config_file.write(config_string)
    yield
    os.remove(config_file_path)


@pytest.fixture
def get_external_object_ids(minio_client):
    def _get_external_object_ids():
        external_objects = minio_client.list_objects(BUCKET_NAME, prefix=MINIO_LOCATION, recursive=True)
        external_object_paths = [obj.object_name for obj in external_objects]
        external_object_names = [path.split("/")[-1] for path in external_object_paths]
        external_object_hashes = [name.split(".")[0] for name in external_object_names]
        return [UUID(hex=obj_hash) for obj_hash in external_object_hashes]

    return _get_external_object_ids


@pytest.fixture
def get_external_table_ids(external_table):
    def _get_external_table_ids():
        return list(external_table.fetch("hash"))

    return _get_external_table_ids


@pytest.mark.usefixtures("configure_dj_cleaner")
def test_if_external_object_ids_match_external_table_ids_after_cleaning(
    insert_entries, delete_entries, get_external_object_ids, get_external_table_ids
):
    insert_entries([1, 2, 3, 4, 5])
    delete_entries([1, 3])
    controller.clean()
    assert get_external_object_ids() == get_external_table_ids()
