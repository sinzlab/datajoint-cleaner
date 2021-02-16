"""Contains the TOML controller."""
from collections.abc import Mapping
from typing import Any, Dict

from ..use_cases.abstract import UseCase
from ..use_cases.clean import CleanRequestModel
from .minio_gateway import MinIOLocation
from .pymysql_gateway import PyMySQLLocation


class TOMLController:
    """Controls the execution of use-cases using TOML formatted configuration information."""

    def __init__(self, use_cases: Mapping[str, UseCase]) -> None:
        """Initialize Controller."""
        self.use_cases = use_cases

    def clean(self, config: Dict[str, Any]) -> None:
        """Execute the clean use-case."""
        for cleaning_run in config["cleaning_runs"]:
            db_server_config = config["database_servers"][cleaning_run["database_server"]]
            storage_server_kind, storage_server_name = cleaning_run["storage_server"].split(".")
            storage_server_config = config["storage_servers"][storage_server_kind][storage_server_name]
            db_location = PyMySQLLocation(cleaning_run["schema"], cleaning_run["store"])
            external_location = MinIOLocation(cleaning_run["schema"], cleaning_run["bucket"], cleaning_run["location"])
            self.use_cases["clean"](
                CleanRequestModel(db_server_config, storage_server_config, db_location, external_location)
            )

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(use_cases={self.use_cases})"
