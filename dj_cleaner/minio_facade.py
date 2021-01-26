"""Contains the facade of the MinIO interface."""
from typing import List, Set

from minio import Minio
from minio.deleteobjects import DeleteObject


class MinIOFacade:
    """Facade of the MinIO interface."""

    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool) -> None:
        """Initialize MinIOFacade."""
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

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
