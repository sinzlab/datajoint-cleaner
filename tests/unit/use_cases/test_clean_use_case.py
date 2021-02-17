import logging
from dataclasses import is_dataclass
from unittest.mock import MagicMock, create_autospec

import pytest
from dj_cleaner.use_cases.abstract import AbstractRequestModel, AbstractResponseModel, AbstractUseCase
from dj_cleaner.use_cases.clean import Clean, CleanRequestModel, CleanResponseModel
from dj_cleaner.use_cases.interfaces import AbstractDatabaseGateway, AbstractStorageGateway


class TestCleanRequestModel:
    def test_if_dataclass(self):
        assert is_dataclass(CleanRequestModel)

    def test_if_subclass_of_abstract_request_model(self):
        assert issubclass(CleanRequestModel, AbstractRequestModel)

    def test_if_annotations_are_correct(self):
        assert all(x in CleanRequestModel.__annotations__ for x in ("db_location", "storage_location"))


class TestCleanResponseModel:
    def test_if_dataclass(self):
        assert is_dataclass(CleanResponseModel)

    def test_if_subclass_of_abstract_response_model(self):
        assert issubclass(CleanResponseModel, AbstractResponseModel)

    def test_if_annotations_are_correct(self):
        assert "n_deleted" in CleanResponseModel.__annotations__


@pytest.fixture
def output_port():
    return MagicMock(name="output_port")


@pytest.fixture
def db_gateway():
    db_gateway = create_autospec(AbstractDatabaseGateway)
    db_gateway.get_ids.return_value = {1, 2, 3}
    return db_gateway


@pytest.fixture
def storage_gateway():
    storage_gateway = create_autospec(AbstractStorageGateway)
    storage_gateway.get_object_ids.return_value = {1, 2, 3, 4}
    return storage_gateway


@pytest.fixture
def use_case(output_port, db_gateway, storage_gateway):
    return Clean(output_port, db_gateway, storage_gateway)


@pytest.fixture
def request_model():
    return MagicMock(name="request_model")


class TestClean:
    def test_if_subclass_of_abstract_use_case(self):
        assert issubclass(Clean, AbstractUseCase)

    def test_if_get_object_ids_of_storage_gateway_is_called_correctly(self, use_case, request_model, storage_gateway):
        use_case(request_model)
        storage_gateway.get_object_ids.assert_called_once_with(request_model.storage_location)

    def test_if_get_ids_of_db_gateway_is_called_correctly(self, use_case, request_model, db_gateway):
        use_case(request_model)
        db_gateway.get_ids.assert_called_once_with(request_model.db_location)

    def test_if_delete_objects_of_storage_gateway_is_called_correctly(self, use_case, request_model, storage_gateway):
        use_case(request_model)
        storage_gateway.delete_objects.assert_called_once_with(request_model.storage_location, {4})

    def test_if_correct_response_model_is_passed_to_output_port(self, use_case, request_model, output_port):
        use_case(request_model)
        output_port.assert_called_once_with(CleanResponseModel(1))

    def test_logged_messages(self, caplog, use_case, request_model):
        with caplog.at_level(logging.INFO):
            use_case(request_model)
            name = "dj_cleaner.use_cases.clean"
            assert caplog.record_tuples == [
                (name, logging.INFO, "Executing clean use-case..."),
                (name, logging.INFO, "Done!"),
            ]
