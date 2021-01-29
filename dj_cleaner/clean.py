"""Contains a simple prototype."""
from __future__ import annotations

import os

from .minio_facade import MinIOFacade
from .minio_gateway import MinIOGateway
from .pymysql_facade import PyMySQLFacade
from .pymysql_gateway import PyMySQLGateway


def clean():
    """Clean up external objects."""
    minio_facade = MinIOFacade(
        endpoint=os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=os.getenv("MINIO_SECURE", "True") == "True",
    )
    minio_gateway = MinIOGateway(
        facade=minio_facade,
        bucket_name=os.environ["MINIO_BUCKET_NAME"],
        location=os.environ["MINIO_LOCATION"],
        schema_name=os.environ["DB_SCHEMA_NAME"],
    )
    minio_object_ids = minio_gateway.get_object_ids()

    pymysql_facade = PyMySQLFacade(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_SCHEMA_NAME"],
    )
    pymysql_gateway = PyMySQLGateway(pymysql_facade, store_name=os.environ["DB_STORE_NAME"])
    db_object_ids = pymysql_gateway.get_ids()

    to_be_deleted_object_ids = minio_object_ids - db_object_ids
    minio_gateway.delete_objects(to_be_deleted_object_ids)
