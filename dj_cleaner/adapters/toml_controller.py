"""Contains the TOML controller."""
from typing import Dict

from ..use_cases.abstract import UseCase
from ..use_cases.clean import CleanRequestModel
from . import FACADE_CONFIGS
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
            db_server_config = config["database_servers"][cleaning_run["database_server"]]
            minio_server_config = config["minio_servers"][cleaning_run["minio_server"]]
            self.config.update(
                {
                    "bucket_name": cleaning_run["bucket"],
                    "location": cleaning_run["location"],
                    "schema_name": cleaning_run["schema"],
                    "store_name": cleaning_run["store"],
                }
            )
            db_config = FACADE_CONFIGS["database"](**db_server_config)
            external_config = FACADE_CONFIGS["minio"](**minio_server_config)
            self.use_cases["clean"](CleanRequestModel(db_config, external_config))

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(config={self.config}, use_cases={self.use_cases})"
