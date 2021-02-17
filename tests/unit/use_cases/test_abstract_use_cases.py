from abc import ABC
from dataclasses import is_dataclass

from dj_cleaner.use_cases.abstract import AbstractRequestModel


class TestAbstractRequestModel:
    def test_if_dataclass(self):
        assert is_dataclass(AbstractRequestModel)

    def test_if_subclass_of_abc(self):
        assert issubclass(AbstractRequestModel, ABC)

    def test_if_annotations_are_correct(self):
        assert all(x in AbstractRequestModel.__annotations__ for x in ("db_config", "storage_config"))
