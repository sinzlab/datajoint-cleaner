"""Contains the definitions of interfaces as expected by the adapters."""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set, TypeVar


class AbstractPyMySQLFacade(ABC):
    """Defines the interface of the PyMySQL facade as expected by the PyMySQL gateway."""

    @abstractmethod
    def execute(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL and return the result."""


PyMySQLFacade = TypeVar("PyMySQLFacade", bound=AbstractPyMySQLFacade)


class AbstractMinIOFacade(ABC):
    """Defines the interface of the MinIO facade as expected by the MinIO gateway."""

    @abstractmethod
    def get_object_paths(self, bucket_name: str, prefix: str) -> List[str]:
        """Get all paths that match the provided prefix of MinIO objects from the bucket."""

    @abstractmethod
    def remove_objects(self, bucket_name: str, object_paths: Set[str]) -> None:
        """Delete the MinIO objects identified by the provided paths from the bucket."""


MinIOFacade = TypeVar("MinIOFacade", bound=AbstractMinIOFacade)
