from dataclasses import is_dataclass
from unittest.mock import MagicMock, create_autospec
from uuid import UUID

import pytest

from dj_cleaner.adapters.interfaces import AbstractMinIOFacade
from dj_cleaner.adapters.minio_gateway import MinIOGateway, MinIOLocation
from dj_cleaner.use_cases.interfaces import AbstractStorageGateway


class TestMinIOLocation:
    def test_if_dataclass(self):
        assert is_dataclass(MinIOLocation)

    def test_if_annotations_are_correct(self):
        assert all(x in MinIOLocation.__annotations__ for x in ("schema_name", "bucket_name", "location"))


@pytest.fixture
def object_paths():
    return [
        "bucket/location/schema/01/2a/065a6c7bc82e4764845b572a350918c6",
        "bucket/location/schema/05/99/06b4462c1cedbe84fc9e1c778ef46415.filename",
    ]


@pytest.fixture
def object_ids():
    return {
        UUID("065a6c7bc82e4764845b572a350918c6"),
        UUID("06b4462c1cedbe84fc9e1c778ef46415"),
    }


@pytest.fixture
def facade(object_paths):
    facade = create_autospec(AbstractMinIOFacade)
    facade.get_object_paths.return_value = object_paths
    facade.__repr__ = MagicMock(name="facade.__repr__", return_value="facade")
    return facade


@pytest.fixture
def gateway(facade):
    return MinIOGateway(facade)


@pytest.fixture
def config():
    return MagicMock(name="config")


@pytest.fixture
def location():
    location = create_autospec(MinIOLocation)
    location.schema_name = "schema"
    location.bucket_name = "bucket"
    location.location = "location"
    return location


class TestMinIOGateway:
    def test_if_subclass_of_abstract_storage_gateway(self):
        assert issubclass(MinIOGateway, AbstractStorageGateway)

    def test_if_facade_is_stored_as_instance_attribute(self, gateway, facade):
        assert gateway.facade is facade

    def test_if_configure_method_of_facade_is_called_correctly(self, gateway, config, facade):
        gateway.configure(config)
        facade.configure.assert_called_once_with(config)

    def test_if_get_object_paths_method_of_facade_is_called_correctly(self, gateway, location, facade):
        gateway.get_object_ids(location)
        facade.get_object_paths.assert_called_once_with("bucket", "location/schema")

    def test_if_correct_object_ids_are_returned(self, gateway, location, object_ids):
        assert gateway.get_object_ids(location) == object_ids

    def test_if_remove_objects_method_of_facade_is_called_correctly(
        self, gateway, location, facade, object_ids, object_paths
    ):
        gateway.get_object_ids(location)
        gateway.delete_objects(location, object_ids)
        facade.remove_objects.assert_called_once_with("bucket", set(object_paths))

    def test_repr(self, gateway):
        assert repr(gateway) == "MinIOGateway(facade=facade)"
