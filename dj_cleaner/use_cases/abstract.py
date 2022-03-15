"""Contains the abstract base class all use-cases must inherit."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from .interfaces import AbstractDatabaseGateway, AbstractStorageGateway


@dataclass
class AbstractRequestModel(ABC):
    """Abstract base class for all request models."""

    db_config: Any
    storage_config: Any


RequestModel = TypeVar("RequestModel", bound=AbstractRequestModel)


@dataclass
class AbstractResponseModel(ABC):
    """Abstract base class for all response models."""


ResponseModel = TypeVar("ResponseModel", bound=AbstractResponseModel)


class AbstractUseCase(ABC, Generic[RequestModel, ResponseModel]):
    """Abstract base class for all use-cases."""

    def __init__(
        self,
        output_port: Callable[[ResponseModel], None],
        db_gateway: AbstractDatabaseGateway,
        storage_gateway: AbstractStorageGateway,
    ) -> None:
        """Initialize the use-case."""
        self.output_port = output_port
        self.db_gateway = db_gateway
        self.storage_gateway = storage_gateway

    def __call__(self, request_model: RequestModel) -> None:
        """Execute the use-case."""
        self.db_gateway.configure(request_model.db_config)
        self.storage_gateway.configure(request_model.storage_config)
        response_model = self._execute(request_model)
        self.output_port(response_model)

    @abstractmethod
    def _execute(self, request_model: RequestModel) -> ResponseModel:
        """Execute the use-case."""

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return (
            f"{self.__class__.__name__}(output_port={self.output_port},"
            f" db_gateway={self.db_gateway}, storage_gateway={self.storage_gateway})"
        )


UseCase = TypeVar("UseCase", bound=AbstractUseCase)
