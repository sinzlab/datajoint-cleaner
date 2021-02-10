"""Contains the TOML controller."""
import os
from typing import Dict

from ..use_cases.abstract import UseCase
from ..use_cases.clean import CleanRequestModel


class TOMLController:
    """Controls the execution of use-cases using TOML formatted configuration information."""

    def __init__(self, config: Dict[str, str], use_cases: Dict[str, UseCase]) -> None:
        """Initialize Controller."""
        self.config = config
        self.use_cases = use_cases

    def clean(self) -> None:
        """Execute the clean use-case."""
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
        self.use_cases["clean"](CleanRequestModel())

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(config={self.config}, use_cases={self.use_cases})"
