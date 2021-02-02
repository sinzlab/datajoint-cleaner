"""Contains a simple prototype."""
from __future__ import annotations

import os
from typing import Dict


class Clean:
    """Clean use-case."""

    def __init__(self, config: Dict[str, str], db_gateway, external_gateway) -> None:
        """Initialize Clean."""
        self.config = config
        self.db_gateway = db_gateway
        self.external_gateway = external_gateway

    def __call__(self) -> None:
        """Clean up external objects."""
        self.config.update(
            {
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
        )

        external_object_ids = self.external_gateway.get_object_ids()
        db_object_ids = self.db_gateway.get_ids()
        to_be_deleted_object_ids = external_object_ids - db_object_ids
        self.external_gateway.delete_objects(to_be_deleted_object_ids)
