"""Contains the facade for the TOML interface."""
from pathlib import Path
from typing import Any, Dict

import toml

from ..adapters.interfaces import AbstractTOMLFacade


class TOMLFacade(AbstractTOMLFacade):
    """Facade for the TOML interface."""

    def __init__(self, filepath: Path) -> None:
        """Initialize TOMLFacade."""
        self.filepath = filepath

    def get_configuration(self) -> Dict[str, Any]:
        """Get the configuration information from the TOML file."""
        return dict(toml.load(self.filepath))
