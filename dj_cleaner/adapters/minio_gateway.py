"""Contains the MinIO gateway."""
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Dict, List, Set
from uuid import UUID

from ..use_cases.interfaces import AbstractExternalGateway
from .interfaces import MinIOFacade


@dataclass
class MinIOLocation:
    """Contains information specifying a certain location in the MinIO server."""

    schema_name: str
    bucket_name: str
    location: str


class MinIOGateway(AbstractExternalGateway):
    """Gateway between the MinIO facade and the use-cases."""

    def __init__(self, facade: MinIOFacade) -> None:
        """Initialize MinIOGateway."""
        self.facade = facade
        self._object_id_to_object_path_mapping: Dict[UUID, str] = {}

    def configure(self, config: Any) -> None:
        """Configure the gateway."""
        self.facade.configure(config)

    def get_object_ids(self, location: MinIOLocation) -> Set[UUID]:
        """Get the IDs of objects stored in the MinIO bucket."""
        object_paths = self._get_object_paths(location)
        object_ids = self._convert_object_paths_to_object_ids(object_paths)
        self._add_object_ids_and_object_paths_to_mapping(object_ids, object_paths)
        return set(object_ids)

    def _get_object_paths(self, location: MinIOLocation) -> List[str]:
        """Get the paths of MinIO objects."""
        prefix = location.location + "/" + location.schema_name
        object_paths = self.facade.get_object_paths(location.bucket_name, prefix=prefix)
        return object_paths

    @staticmethod
    def _convert_object_paths_to_object_ids(paths: Sequence[str]) -> List[UUID]:
        """Convert MinIO object paths to object IDs."""
        object_names = [x.split("/")[-1] for x in paths]
        object_names = [x.split(".")[0] for x in object_names]
        object_ids = [UUID(x) for x in object_names]
        return object_ids

    def _add_object_ids_and_object_paths_to_mapping(
        self, object_ids: Sequence[UUID], object_paths: Sequence[str]
    ) -> None:
        for object_id, object_path in zip(object_ids, object_paths):
            self._object_id_to_object_path_mapping[object_id] = object_path

    def _convert_object_ids_to_object_paths(self, object_ids: Set[UUID]) -> Set[str]:
        """Convert object IDs to MinIO object paths."""
        object_paths = {self._object_id_to_object_path_mapping[x] for x in object_ids}
        return object_paths

    def delete_objects(self, location: MinIOLocation, object_ids: Set[UUID]) -> None:
        """Delete the objects specified by the provided object IDs from the MinIO bucket."""
        object_paths = self._convert_object_ids_to_object_paths(object_ids)
        self.facade.remove_objects(location.bucket_name, object_paths)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(facade={self.facade})"
