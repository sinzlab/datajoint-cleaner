"""Contains the PyMySQL gateway."""
from dataclasses import dataclass
from typing import Any, Set
from uuid import UUID

from ..use_cases.interfaces import AbstractDatabaseGateway
from .interfaces import PyMySQLFacade


@dataclass
class PyMySQLLocation:
    """Contains information specifying a certain location in the datbase server."""

    schema_name: str
    store_name: str


class PyMySQLGateway(AbstractDatabaseGateway):
    """Gateway between the PyMySQL facade and the use cases."""

    def __init__(self, facade: PyMySQLFacade) -> None:
        """Initialize PyMySQLGateway."""
        self.facade = facade

    def configure(self, config: Any) -> None:
        """Configure the gateway."""
        self.facade.configure(config)

    def get_ids(self, location: PyMySQLLocation) -> Set[UUID]:
        """Get the IDs of entities stored in the external table."""
        external_table_name = "~external_" + location.store_name
        sql = f"SELECT `hash` from `{external_table_name}`"
        hashes = self.facade.execute(location.schema_name, sql)
        object_ids = {UUID(bytes=h["hash"]) for h in hashes}
        return object_ids

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(facade={self.facade})"
