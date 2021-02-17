from unittest.mock import create_autospec

import pytest
from dj_cleaner.adapters.toml_presenter import TOMLPresenter
from dj_cleaner.use_cases.clean import CleanResponseModel


@pytest.fixture
def response_model():
    response_model = create_autospec(CleanResponseModel)
    response_model.n_deleted = 10000
    return response_model


@pytest.fixture
def toml_presenter():
    return TOMLPresenter()


def test_if_correct_message_is_printed_after_cleaning(capsys, toml_presenter, response_model):
    toml_presenter.clean(response_model)
    captured = capsys.readouterr()
    assert captured.out == "Deleted 10,000 objects from external storage.\n"


def test_repr(toml_presenter):
    assert repr(toml_presenter) == "TOMLPresenter()"
