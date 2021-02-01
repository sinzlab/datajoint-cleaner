"""Contains the definitions of the database/external gateway interfaces."""
from abc import ABC, abstractmethod
from typing import Set
from uuid import UUID


class AbstractDatabaseGateway(ABC):
    """Defines the interface of the database gateway as expected by the use-cases."""

    @abstractmethod
    def get_ids(self) -> Set[UUID]:
        """Get the IDs of entities stored in the external table."""


class AbstractExternalGateway(ABC):
    """Defines the interface of the external gateway as expected by the use-cases."""

    @abstractmethod
    def get_object_ids(self) -> Set[UUID]:
        """Get the IDs of all objects stored in the external store."""

    @abstractmethod
    def delete_objects(self, object_ids: Set[UUID]) -> None:
        """Delete the objects specified by the provided object IDs from the external store."""
