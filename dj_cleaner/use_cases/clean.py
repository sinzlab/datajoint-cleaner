"""Contains a simple prototype."""
from __future__ import annotations

from .abstract import UseCase
from .interfaces import AbstractDatabaseGateway, AbstractExternalGateway


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
