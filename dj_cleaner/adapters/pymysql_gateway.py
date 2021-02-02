"""Contains the PyMySQL gateway."""
from typing import Dict, Set
from uuid import UUID

from ..frameworks.pymysql_facade import PyMySQLFacade
from ..use_cases.interfaces import AbstractDatabaseGateway


class PyMySQLGateway(AbstractDatabaseGateway):
    """Gateway between the PyMySQL facade and the use cases."""

    def __init__(self, facade: PyMySQLFacade, config: Dict[str, str]) -> None:
        """Initialize PyMySQLGateway."""
        self.facade = facade
        self.config = config

    def get_ids(self) -> Set[UUID]:
        """Get the IDs of entities stored in the external table."""
        external_table_name = "~external_" + self.config["store_name"]
        sql = f"SELECT `hash` from `{external_table_name}`"
        hashes = self.facade.execute(sql)
        object_ids = {UUID(bytes=h["hash"]) for h in hashes}
        return object_ids
