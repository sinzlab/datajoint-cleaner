"""Contains the facade of the MinIO interface."""
from typing import Dict, List, Optional, Set

from minio import Minio
from minio.deleteobjects import DeleteObject


class MinIOFacade:
    """Facade of the MinIO interface."""

    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize MinIOFacade."""
        self.config = config
        self._client: Optional[Minio] = None  # pylint: disable=unsubscriptable-object

    @property
    def client(self) -> Minio:
        """Return already instantiated MinIO client if possible or instantiate and return a new one."""
        if not self._client:
            self._client = Minio(
                self.config["endpoint"],
                access_key=self.config["access_key"],
                secret_key=self.config["secret_key"],
                secure=self.config["secure"] == "True",
            )
        return self._client

    def get_object_paths(self, bucket_name: str, prefix: str) -> List[str]:
        """Get all paths that match the provided prefix of MinIO objects from the bucket."""
        objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
        object_paths = [x.object_name for x in objects]
        return object_paths

    def remove_objects(self, bucket_name: str, object_paths: Set[str]) -> None:
        """Delete the MinIO objects identified by the provided paths from the bucket."""
        delete_object_list = [DeleteObject(x) for x in object_paths]
        errors = self.client.remove_objects(bucket_name, delete_object_list=delete_object_list)
        for error in errors:
            print(error)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(config={self.config})"
