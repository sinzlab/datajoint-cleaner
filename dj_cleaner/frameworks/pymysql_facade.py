"""Contains the facade of the PyMySQL interface."""
from typing import Any, Dict, List, Optional, Type

from pymysql import connect
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from ..adapters.interfaces import AbstractFacadeConfig, AbstractPyMySQLFacade


class PyMySQLFacadeConfig(AbstractFacadeConfig):
    """Configuration for the PyMySQL facade."""

    def __init__(self, host: str, user: str, password: str):
        """Initialize PyMySQLFacadeConfig."""
        self.host = host
        self.user = user
        self.password = password

    def to_dict(self) -> Dict[str, str]:
        """Return configuration as a dictionary."""
        return {"host": self.host, "user": self.user, "password": self.password}


class PyMySQLFacade(AbstractPyMySQLFacade[Type[PyMySQLFacadeConfig]]):
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
        self._connection = connect(cursorclass=DictCursor, **config.to_dict())

    def execute(self, database: str, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL against the provided database and return the result."""
        self.connection.select_db(database)
        with self.connection:  # type: ignore
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result  # type: ignore

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}()"
