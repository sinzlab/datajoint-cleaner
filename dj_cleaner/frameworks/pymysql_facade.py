"""Contains the facade of the PyMySQL interface."""
from typing import Any, Dict, List, Optional

from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from ..adapters.interfaces import AbstractPyMySQLFacade


class PyMySQLFacade(AbstractPyMySQLFacade):
    """Facade for the PyMySQL interface."""

    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize PyMySQLFacade."""
        self.config = config
        self._connection: Optional[Connection] = None  # pylint: disable=unsubscriptable-object

    @property
    def connection(self) -> Connection:
        """Return already instantiated PyMySQL connection if possible or instantiate and return a new one."""
        if not self._connection:
            self._connection = connect(
                host=self.config["host"],
                user=self.config["user"],
                password=self.config["password"],
                database=self.config["database"],
                cursorclass=DictCursor,
            )
        return self._connection

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL and return the result."""
        with self.connection:  # type: ignore
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result  # type: ignore

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(config={self.config})"
