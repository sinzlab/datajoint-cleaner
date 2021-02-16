"""Contains a simple prototype."""
import logging
from dataclasses import dataclass
from typing import Any

from .abstract import AbstractRequestModel, AbstractUseCase

LOGGER = logging.getLogger(__name__)


@dataclass
class CleanRequestModel(AbstractRequestModel):
    """Request model for the clean use-case."""

    db_location: Any
    storage_location: Any


class Clean(AbstractUseCase[CleanRequestModel]):  # pylint: disable=too-few-public-methods, unsubscriptable-object
    """Clean use-case."""

    def _execute(self, request_model: CleanRequestModel) -> None:
        """Clean up superfluous objects."""
        LOGGER.info("Executing clean use-case...")
        storage_object_ids = self.storage_gateway.get_object_ids(request_model.storage_location)
        db_object_ids = self.db_gateway.get_ids(request_model.db_location)
        to_be_deleted_object_ids = storage_object_ids - db_object_ids
        self.storage_gateway.delete_objects(request_model.storage_location, to_be_deleted_object_ids)
        LOGGER.info("Done!")
