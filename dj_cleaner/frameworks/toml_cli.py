"""Contains the TOML command line interface."""
import logging
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

import toml

from ..adapters.toml_controller import TOMLController

LOGGER = logging.getLogger(__name__)


class TOMLCLI:
    """Command line interface using TOML configuration file."""

    def __init__(self, controller: TOMLController) -> None:
        """Initialize TOMLCLI."""
        self.controller = controller
        self.parser = ArgumentParser(description="Clean up external DataJoint stores.")
        self.parser.add_argument(
            "-c",
            "--config-file",
            default="datajoint-cleaner.toml",
            type=Path,
            help="Path to configuration file",
            dest="config_file",
        )
        self.parser.add_argument("--log-file", default=None, type=Path, help="Path to log file", dest="log_file")
        self.parser.add_argument("--log-level", default="WARNING", help="Logging level", dest="log_level")

    def clean(self, args: Sequence[str]) -> None:
        """Execute clean use-case."""
        parsed_args = self.parser.parse_args(args)
        self._configure_logging(parsed_args)
        LOGGER.info("Starting cleaning")
        config = dict(toml.load(parsed_args.config_file))
        LOGGER.info(f"Loaded TOML config file from {parsed_args.config_file}")
        self.controller.clean(config)
        LOGGER.info("Finished cleaning")

    @staticmethod
    def _configure_logging(parsed_args) -> None:
        if parsed_args.log_file is None:
            return
        numeric_level = getattr(logging, parsed_args.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {parsed_args.log_level}")
        format_string = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
        logging.basicConfig(filename=parsed_args.log_file, level=numeric_level, format=format_string)
