"""Contains the abstract base class all use-cases must inherit."""
from abc import ABC, abstractmethod

from .interfaces import AbstractDatabaseGateway, AbstractExternalGateway


class UseCase(ABC):
    """Abstract base class for all use-cases."""

    def __init__(self, db_gateway: AbstractDatabaseGateway, external_gateway: AbstractExternalGateway) -> None:
        """Initialize Clean."""
        self.db_gateway = db_gateway
        self.external_gateway = external_gateway

    def __call__(self) -> None:
        """Execute the use-case."""
        self._execute()

    @abstractmethod
    def _execute(self) -> None:
        """Execute the use-case."""

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(db_gateway={self.db_gateway}, external_gateway={self.external_gateway})"
