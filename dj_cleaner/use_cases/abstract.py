"""Contains the abstract base class all use-cases must inherit."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from .interfaces import AbstractDatabaseGateway, AbstractExternalGateway


@dataclass
class AbstractRequestModel(ABC):
    """Abstract base class for all request-models."""

    db_config: Any
    external_config: Any


RequestModel = TypeVar("RequestModel", bound=AbstractRequestModel)


class AbstractUseCase(ABC, Generic[RequestModel]):
    """Abstract base class for all use-cases."""

    def __init__(self, db_gateway: AbstractDatabaseGateway, external_gateway: AbstractExternalGateway) -> None:
        """Initialize Clean."""
        self.db_gateway = db_gateway
        self.external_gateway = external_gateway

    def __call__(self, request_model: RequestModel) -> None:
        """Execute the use-case."""
        self.db_gateway.configure(request_model.db_config)
        self.external_gateway.configure(request_model.external_config)
        self._execute(request_model)

    @abstractmethod
    def _execute(self, request_model: RequestModel) -> None:
        """Execute the use-case."""

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(db_gateway={self.db_gateway}, external_gateway={self.external_gateway})"


UseCase = TypeVar("UseCase", bound=AbstractUseCase)
