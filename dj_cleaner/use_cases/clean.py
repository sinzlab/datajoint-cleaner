"""Contains a simple prototype."""
from dataclasses import dataclass
from typing import Any

from .abstract import AbstractRequestModel, AbstractUseCase


@dataclass
class CleanRequestModel(AbstractRequestModel):
    """Request model for the clean use-case."""

    db_location: Any
    external_location: Any


class Clean(AbstractUseCase[CleanRequestModel]):  # pylint: disable=too-few-public-methods, unsubscriptable-object
    """Clean use-case."""

    def _execute(self, request_model: CleanRequestModel) -> None:
        """Clean up external objects."""
        external_object_ids = self.external_gateway.get_object_ids(request_model.external_location)
        db_object_ids = self.db_gateway.get_ids(request_model.db_location)
        to_be_deleted_object_ids = external_object_ids - db_object_ids
        self.external_gateway.delete_objects(request_model.external_location, to_be_deleted_object_ids)
