"""Contains a simple prototype."""
from __future__ import annotations

import os

from .minio_facade import MinIOFacade
from .minio_gateway import MinIOGateway
from .pymysql_facade import PyMySQLFacade
from .pymysql_gateway import PyMySQLGateway


def clean() -> None:
    """Clean up external objects."""
    config = {
        "endpoint": os.environ["MINIO_ENDPOINT"],
        "access_key": os.environ["MINIO_ACCESS_KEY"],
        "secret_key": os.environ["MINIO_SECRET_KEY"],
        "secure": os.environ["MINIO_SECURE"],
        "bucket_name": os.environ["MINIO_BUCKET_NAME"],
        "location": os.environ["MINIO_LOCATION"],
        "schema_name": os.environ["DB_SCHEMA_NAME"],
        "host": os.environ["DB_HOST"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_SCHEMA_NAME"],
        "store_name": os.environ["DB_STORE_NAME"],
    }

    minio_facade = MinIOFacade(config)
    minio_gateway = MinIOGateway(facade=minio_facade, config=config)
    minio_object_ids = minio_gateway.get_object_ids()

    pymysql_facade = PyMySQLFacade(config)
    pymysql_gateway = PyMySQLGateway(facade=pymysql_facade, config=config)
    db_object_ids = pymysql_gateway.get_ids()

    to_be_deleted_object_ids = minio_object_ids - db_object_ids
    minio_gateway.delete_objects(to_be_deleted_object_ids)
