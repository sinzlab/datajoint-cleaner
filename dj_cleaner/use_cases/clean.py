"""Contains a simple prototype."""
from .abstract import UseCase


class Clean(UseCase):  # pylint: disable=too-few-public-methods
    """Clean use-case."""

    def _execute(self) -> None:
        """Clean up external objects."""
        external_object_ids = self.external_gateway.get_object_ids()
        db_object_ids = self.db_gateway.get_ids()
        to_be_deleted_object_ids = external_object_ids - db_object_ids
        self.external_gateway.delete_objects(to_be_deleted_object_ids)
