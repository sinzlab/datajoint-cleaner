"""Contains the definitions of interfaces as expected by the adapters."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Set, Type, TypeVar


class AbstractFacadeConfig(ABC):
    """Abstract base class for all facade configs."""

    @abstractmethod
    def __init__(self, **kwargs) -> None:
        """Initialize AbstractFacadeConfig."""


FacadeConfig = TypeVar("FacadeConfig", bound=Type[AbstractFacadeConfig])


class AbstractFacade(ABC, Generic[FacadeConfig]):
    """Abstract base class for all facades."""

    @abstractmethod
    def configure(self, config: Any) -> None:
        """Configure the facade."""


class AbstractPyMySQLFacade(AbstractFacade[FacadeConfig]):
    """Defines the interface of the PyMySQL facade as expected by the PyMySQL gateway."""

    @abstractmethod
    def execute(self, database: str, sql: str) -> List[Dict[str, Any]]:
        """Execute SQL against the provided database and return the result."""


PyMySQLFacade = TypeVar("PyMySQLFacade", bound=AbstractPyMySQLFacade)


class AbstractMinIOFacade(AbstractFacade[FacadeConfig]):
    """Defines the interface of the MinIO facade as expected by the MinIO gateway."""

    @abstractmethod
    def get_object_paths(self, bucket_name: str, prefix: str) -> List[str]:
        """Get all paths that match the provided prefix of MinIO objects from the bucket."""

    @abstractmethod
    def remove_objects(self, bucket_name: str, object_paths: Set[str]) -> None:
        """Delete the MinIO objects identified by the provided paths from the bucket."""


MinIOFacade = TypeVar("MinIOFacade", bound=AbstractMinIOFacade)


class AbstractTOMLFacade(ABC):
    """Defines the interface of the TOML facade as expected by the TOML controller."""

    @abstractmethod
    def get_configuration(self) -> Dict[str, Any]:
        """Get the configuration information from the TOML file."""


TOMLFacade = TypeVar("TOMLFacade", bound=AbstractTOMLFacade)
