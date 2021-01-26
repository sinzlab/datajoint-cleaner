import os
import time
from tempfile import TemporaryDirectory
from uuid import UUID

import datajoint as dj
import docker
import pytest
from dj_cleaner import main
from minio import Minio

HEALTH_CHECK_MAX_RETRIES = 60
HEALTH_CHECK_INTERVAL = 1

DJ_MYSQL_IMAGE_TAG = "8.0.18-slim-827c535"
DB_HOST = "localhost"
DJ_MYSQL_ROOT_PASSWORD = "simple"
DJ_MYSQL_PORT = 3306

MINIO_IMAGE_TAG = "latest"
MINIO_ENDPOINT = "localhost"
MINIO_ACCESS_KEY = "access_key"
MINIO_SECRET_KEY = "secret_key"
MINIO_PORT = 9000
MINIO_HEALTHCHECK_START_PERIOD = 0
MINIO_HEALTHCHECK_INTERVAL = 60
MINIO_HEALTHCHECK_RETRIES = 1
MINIO_HEALTHCHECK_TIMEOUT = 5

STORE_NAME = "external"
BUCKET_NAME = "my-bucket"
LOCATION = "dj-store"
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
def dj_mysql_container(run_container):
    container_config = {
        "image": "datajoint/mysql:" + DJ_MYSQL_IMAGE_TAG,
        "detach": True,
        "auto_remove": True,
        "name": "dj-mysql",
        "environment": {"MYSQL_ROOT_PASSWORD": DJ_MYSQL_ROOT_PASSWORD},
        "ports": {DJ_MYSQL_PORT: DJ_MYSQL_PORT},
    }
    with run_container(container_config):
        yield


@pytest.fixture
def minio_container(run_container):
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


def test_clean(dj_mysql_container, minio_container):
    dj.config["database.host"] = "localhost"
    dj.config["database.user"] = "root"
    dj.config["database.password"] = DJ_MYSQL_ROOT_PASSWORD
    dj.config["stores"] = {
        STORE_NAME: {
            "protocol": "s3",
            "endpoint": "localhost:" + str(MINIO_PORT),
            "bucket": BUCKET_NAME,
            "location": LOCATION,
            "access_key": MINIO_ACCESS_KEY,
            "secret_key": MINIO_SECRET_KEY,
        }
    }
    schema = dj.schema(SCHEMA_NAME)

    @schema
    class MyTable(dj.Manual):
        definition = f"""
        primary_attr    : int
        ---
        attached_attr   : attach@{STORE_NAME}
        """

    minio_client = Minio(
        endpoint="localhost:" + str(MINIO_PORT), access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False
    )
    minio_client.make_bucket(BUCKET_NAME)

    with TemporaryDirectory() as temp_dir_name:
        filenames = ["file" + str(i) for i in range(5)]
        filepaths = [os.path.join(temp_dir_name, fn) for fn in filenames]
        for filepath in filepaths:
            with open(filepath, "wb") as file:
                file.write(os.urandom(1024))
        MyTable.insert([{"primary_attr": i, "attached_attr": fp} for i, fp in enumerate(filepaths)])

    to_be_deleted = [1, 3]
    for i in to_be_deleted:
        (MyTable() & "primary_attr = " + str(i)).delete_quick()
        del filenames[i]
        del filepaths[i]

    schema.external[STORE_NAME].delete(delete_external_files=False)

    os.environ["MINIO_ENDPOINT"] = MINIO_ENDPOINT + ":" + str(MINIO_PORT)
    os.environ["MINIO_ACCESS_KEY"] = MINIO_ACCESS_KEY
    os.environ["MINIO_SECRET_KEY"] = MINIO_SECRET_KEY
    os.environ["MINIO_BUCKET_NAME"] = BUCKET_NAME
    os.environ["MINIO_LOCATION"] = LOCATION
    os.environ["MINIO_SECURE"] = "False"
    os.environ["DB_SCHEMA_NAME"] = SCHEMA_NAME
    os.environ["DB_HOST"] = DB_HOST
    os.environ["DB_USER"] = "root"
    os.environ["DB_PASSWORD"] = DJ_MYSQL_ROOT_PASSWORD
    os.environ["DB_STORE_NAME"] = STORE_NAME
    main.main()

    external_objects = minio_client.list_objects(BUCKET_NAME, prefix=LOCATION, recursive=True)
    external_object_paths = [obj.object_name for obj in external_objects]
    external_object_names = [path.split("/")[-1] for path in external_object_paths]
    external_object_hashes = [name.split(".")[0] for name in external_object_names]
    external_object_ids = [UUID(hex=obj_hash) for obj_hash in external_object_hashes]

    external_table_ids = list(schema.external[STORE_NAME].fetch("hash"))

    assert external_object_ids == external_table_ids
