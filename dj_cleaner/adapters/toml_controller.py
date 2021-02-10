"""Contains the TOML controller."""
from typing import Dict

from ..use_cases.abstract import UseCase
from ..use_cases.clean import CleanRequestModel
from .interfaces import TOMLFacade


class TOMLController:
    """Controls the execution of use-cases using TOML formatted configuration information."""

    def __init__(self, facade: TOMLFacade, config: Dict[str, str], use_cases: Dict[str, UseCase]) -> None:
        """Initialize Controller."""
        self.facade = facade
        self.config = config
        self.use_cases = use_cases

    def clean(self) -> None:
        """Execute the clean use-case."""
        config = self.facade.get_configuration()
        for cleaning_run in config["cleaning_runs"]:
            db_server_config = config["database_servers"][cleaning_run["database"]]
            minio_server_config = config["minio_servers"][cleaning_run["minio"]]
            self.config.update(
                {
                    "endpoint": minio_server_config["endpoint"],
                    "access_key": minio_server_config["access_key"],
                    "secret_key": minio_server_config["secret_key"],
                    "secure": minio_server_config["secure"],
                    "bucket_name": cleaning_run["bucket"],
                    "location": cleaning_run["location"],
                    "schema_name": cleaning_run["schema"],
                    "host": db_server_config["host"],
                    "user": db_server_config["user"],
                    "password": db_server_config["password"],
                    "database": cleaning_run["schema"],
                    "store_name": cleaning_run["store"],
                }
            )
            self.use_cases["clean"](CleanRequestModel())

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(config={self.config}, use_cases={self.use_cases})"
