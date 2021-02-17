from abc import ABC
from dataclasses import is_dataclass
from unittest.mock import MagicMock, create_autospec

import pytest

from dj_cleaner.use_cases.abstract import AbstractRequestModel, AbstractResponseModel, AbstractUseCase
from dj_cleaner.use_cases.interfaces import AbstractDatabaseGateway, AbstractStorageGateway


class TestAbstractRequestModel:
    def test_if_dataclass(self):
        assert is_dataclass(AbstractRequestModel)

    def test_if_subclass_of_abc(self):
        assert issubclass(AbstractRequestModel, ABC)

    def test_if_annotations_are_correct(self):
        assert all(x in AbstractRequestModel.__annotations__ for x in ("db_config", "storage_config"))


class TestAbstractResponseModel:
    def test_if_dataclass(self):
        assert is_dataclass(AbstractResponseModel)

    def test_if_subclass_of_abc(self):
        assert issubclass(AbstractResponseModel, ABC)


@pytest.fixture
def output_port():
    name = "output_port"
    output_port = MagicMock(name=name)
    output_port.__repr__ = MagicMock(name=name + ".__repr__", return_value=name)
    return output_port


@pytest.fixture
def db_gateway():
    name = "db_gateway"
    db_gateway = create_autospec(AbstractDatabaseGateway)
    db_gateway.__repr__ = MagicMock(name=name + ".__repr__", return_value=name)
    return db_gateway


@pytest.fixture
def storage_gateway():
    name = "storage_gateway"
    storage_gateway = create_autospec(AbstractStorageGateway)
    storage_gateway.__repr__ = MagicMock(name=name + ".__repr__", return_value=name)
    return storage_gateway


@pytest.fixture
def use_case(output_port, db_gateway, storage_gateway):
    class UseCase(AbstractUseCase):
        def _execute(self, request_model):
            return "response_model"

    return UseCase(output_port, db_gateway, storage_gateway)


@pytest.fixture
def request_model():
    return MagicMock(name="request_model")


class TestAbstractUseCase:
    def test_if_subclass_of_abc(self):
        assert issubclass(AbstractUseCase, ABC)

    def test_if_output_port_is_stored_as_instance_attribute(self, use_case, output_port):
        assert use_case.output_port is output_port

    def test_if_db_gateway_is_stored_as_instance_attribute(self, use_case, db_gateway):
        assert use_case.db_gateway is db_gateway

    def test_if_storage_gateway_is_stored_as_instance_attribute(self, use_case, storage_gateway):
        assert use_case.storage_gateway is storage_gateway

    def test_if_configure_method_of_db_gateway_is_called_correctly(self, use_case, request_model, db_gateway):
        use_case(request_model)
        db_gateway.configure.assert_called_once_with(request_model.db_config)

    def test_if_configure_method_of_storage_gateway_is_called_correctly(self, use_case, request_model, storage_gateway):
        use_case(request_model)
        storage_gateway.configure.assert_called_once_with(request_model.storage_config)

    def test_if_output_port_is_called_correctly(self, use_case, request_model, output_port):
        use_case(request_model)
        output_port.assert_called_once_with("response_model")

    def test_repr(self, use_case):
        assert (
            repr(use_case) == "UseCase(output_port=output_port, db_gateway=db_gateway, storage_gateway=storage_gateway)"
        )
