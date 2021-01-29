"""Contains the facade of the PyMySQL interface."""
from typing import Any, Dict, List

from pymysql import connect
from pymysql.cursors import DictCursor


class PyMySQLFacade:
    """Facade for the PyMySQL interface."""

    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        """Initialize PyMySQLFacade."""
        self.connection = connect(host=host, user=user, password=password, database=database, cursorclass=DictCursor)

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL and return the result."""
        with self.connection:  # type: ignore
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result  # type: ignore
