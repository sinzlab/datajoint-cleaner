"""Contains a simple prototype."""
from __future__ import annotations

import os
from typing import Set
from uuid import UUID

import pymysql

from .minio_facade import MinIOFacade
from .minio_gateway import MinIOGateway


def main():
    """Run main."""
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
    db_object_ids = get_db_object_ids()
    to_be_deleted_object_ids = minio_object_ids - db_object_ids
    minio_gateway.delete_objects(to_be_deleted_object_ids)


def get_db_object_ids() -> Set[UUID]:
    """Get database object IDs."""
    connection = pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_SCHEMA_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    with connection:  # type: ignore
        with connection.cursor() as cursor:
            external_table_name = "~external_" + os.environ["DB_STORE_NAME"]
            sql = f"SELECT `hash` from `{external_table_name}`"
            cursor.execute(sql)
            result = cursor.fetchall()
            object_ids = {x["hash"] for x in result}  # type: ignore
            object_ids = {UUID(bytes=h) for h in object_ids}
            return object_ids


if __name__ == "__main__":
    main()
