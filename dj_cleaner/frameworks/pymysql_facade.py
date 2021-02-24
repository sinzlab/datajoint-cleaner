"""Contains the facade of the PyMySQL interface."""
import logging
from typing import Any, Dict, List, Optional, TypedDict

from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from ..adapters.interfaces import AbstractPyMySQLFacade

LOGGER = logging.getLogger(__name__)


class PyMySQLFacadeConfig(TypedDict):  # pylint: disable=inherit-non-class, too-few-public-methods
    """Configuration for the PyMySQL facade."""

    host: str
    user: str
    password: str


class PyMySQLFacade(AbstractPyMySQLFacade):
    """Facade for the PyMySQL interface."""

    def __init__(self) -> None:
        """Initialize PyMySQLFacade."""
        self._connection: Optional[Connection] = None  # pylint: disable=unsubscriptable-object

    @property
    def connection(self) -> Connection:
        """Return already instantiated PyMySQL connection if possible or instantiate and return a new one."""
        if not self._connection:
            raise RuntimeError(f"{self.__class__.__name__} is not configured")
        return self._connection

    def configure(self, config: PyMySQLFacadeConfig) -> None:
        """Configure the facade."""
        self._connection = connect(cursorclass=DictCursor, **config)
        LOGGER.info(f"Established connection to PyMySQL server at {config['host']}")

    def execute(self, database: str, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL against the provided database and return the result."""
        LOGGER.info(f"Executing sql {sql} against database {database}...")
        self.connection.select_db(database)
        with self.connection:  # type: ignore
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                LOGGER.info("Done!")
                return result  # type: ignore

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}()"
