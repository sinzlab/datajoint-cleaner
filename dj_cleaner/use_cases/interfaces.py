"""Contains the definitions of interfaces as expected by the use-cases."""
from abc import ABC, abstractmethod
from typing import Any, Set
from uuid import UUID


class AbstractGateway(ABC):
    """Abstract base class for all gateways."""

    @abstractmethod
    def configure(self, config: Any) -> None:
        """Configure the gateway."""


class AbstractDatabaseGateway(AbstractGateway):
    """Defines the interface of the database gateway as expected by the use-cases."""

    @abstractmethod
    def get_ids(self, location: Any) -> Set[UUID]:
        """Get the IDs of entities stored in the database."""


class AbstractExternalGateway(AbstractGateway):
    """Defines the interface of the external gateway as expected by the use-cases."""

    @abstractmethod
    def get_object_ids(self, location: Any) -> Set[UUID]:
        """Get the IDs of all objects stored in the external store."""

    @abstractmethod
    def delete_objects(self, location: Any, object_ids: Set[UUID]) -> None:
        """Delete the objects specified by the provided object IDs from the external store."""
