"""Contains the PyMySQL gateway."""
from typing import Set
from uuid import UUID

from .pymysql_facade import PyMySQLFacade


class PyMySQLGateway:
    """Gateway between the PyMySQL facade and the use cases."""

    def __init__(self, facade: PyMySQLFacade, store_name: str) -> None:
        """Initialize PyMySQLGateway."""
        self.facade = facade
        self.store_name = store_name

    def get_ids(self) -> Set[UUID]:
        """Get the IDs of entities stored in the external table."""
        external_table_name = "~external_" + self.store_name
        sql = f"SELECT `hash` from `{external_table_name}`"
        hashes = self.facade.execute(sql)
        object_ids = {UUID(bytes=h["hash"]) for h in hashes}
        return object_ids
