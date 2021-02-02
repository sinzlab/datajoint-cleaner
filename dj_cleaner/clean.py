"""Contains a simple prototype."""
from __future__ import annotations

from abc import ABC, abstractmethod

from .abstract import AbstractDatabaseGateway, AbstractExternalGateway


class UseCase(ABC):
    """Abstract base class for all use-cases."""

    def __call__(self) -> None:
        """Execute the use-case."""
        self._execute()

    @abstractmethod
    def _execute(self) -> None:
        """Execute the use-case."""


class Clean(UseCase):
    """Clean use-case."""

    def __init__(self, db_gateway: AbstractDatabaseGateway, external_gateway: AbstractExternalGateway) -> None:
        """Initialize Clean."""
        self.db_gateway = db_gateway
        self.external_gateway = external_gateway

    def _execute(self) -> None:
        """Clean up external objects."""
        external_object_ids = self.external_gateway.get_object_ids()
        db_object_ids = self.db_gateway.get_ids()
        to_be_deleted_object_ids = external_object_ids - db_object_ids
        self.external_gateway.delete_objects(to_be_deleted_object_ids)
