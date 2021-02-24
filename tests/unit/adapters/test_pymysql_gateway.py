from dataclasses import is_dataclass
from unittest.mock import MagicMock, create_autospec
from uuid import UUID

import pytest

from dj_cleaner.adapters.pymysql_gateway import PyMySQLGateway, PyMySQLLocation
from dj_cleaner.frameworks.pymysql_facade import PyMySQLFacade
from dj_cleaner.use_cases.interfaces import AbstractDatabaseGateway


class TestPyMySQLLocation:
    def test_if_dataclass(self):
        assert is_dataclass(PyMySQLLocation)

    def test_if_annotations_are_correct(self):
        assert all(x in PyMySQLLocation.__annotations__ for x in ("schema_name", "store_name"))


def test_if_subclass_of_abstract_database_gateway():
    assert issubclass(PyMySQLGateway, AbstractDatabaseGateway)


@pytest.fixture
def hashes():
    hashes = [
        b"\x11\xdc\x8b\xc5\xe9\x08c\xf9B\x1e.d\xb5E\x11r",
        b"\xf0\xe6g\x13%\n\x90\t\xb3\xabs\x13\xedw@&",
        b"~gN\x937k\x82^\xeet\xfa\x8d\x7f\xae\x84>",
    ]
    return [{"hash": h} for h in hashes]


@pytest.fixture
def facade(hashes):
    facade = create_autospec(PyMySQLFacade)
    facade.execute.return_value = hashes
    facade.__repr__ = MagicMock(return_value="Facade()")
    return facade


@pytest.fixture
def store_name():
    return "my-store"


@pytest.fixture
def schema_name():
    return "my_schema"


@pytest.fixture
def location(schema_name, store_name):
    location = create_autospec(PyMySQLLocation)
    location.schema_name = schema_name
    location.store_name = store_name
    return location


@pytest.fixture
def gateway(facade):
    return PyMySQLGateway(facade=facade)


def test_if_facade_is_stored_as_instance_attribute(gateway, facade):
    assert gateway.facade is facade


def test_if_configure_method_of_facade_is_called_correctly(gateway, config, facade):
    gateway.configure(config)
    facade.configure.assert_called_once_with(config)


def test_if_execute_method_of_facade_is_called_correctly_when_getting_ids(
    gateway, facade, location, store_name, schema_name
):
    gateway.get_ids(location)
    external_store_name = "~external_" + store_name
    facade.execute.assert_called_once_with(schema_name, f"SELECT `hash` from `{external_store_name}`")


def test_if_correct_object_ids_are_returned(gateway, hashes, location):
    assert gateway.get_ids(location) == {UUID(bytes=h["hash"]) for h in hashes}


def test_repr(gateway, facade):
    assert repr(gateway) == f"PyMySQLGateway(facade={facade})"
