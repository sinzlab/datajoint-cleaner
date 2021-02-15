"""Contains the TOML command line interface."""
from argparse import ArgumentParser
from collections.abc import Sequence
from pathlib import Path

import toml

from ..adapters.toml_controller import TOMLController


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

    def clean(self, args: Sequence[str]) -> None:
        """Execute clean use-case."""
        parsed_args = self.parser.parse_args(args)
        config = dict(toml.load(parsed_args.config_file))
        self.controller.clean(config)
