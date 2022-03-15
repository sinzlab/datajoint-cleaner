import logging
import os
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, create_autospec

import pytest

from dj_cleaner.adapters.toml_controller import TOMLController
from dj_cleaner.frameworks.toml_cli import TOMLCLI


@pytest.fixture
def controller():
    controller = create_autospec(TOMLController)
    controller.__repr__ = MagicMock(name="controller.__repr__", return_value="controller")
    return controller


@pytest.fixture
def toml_cli(controller):
    return TOMLCLI(controller)


@pytest.fixture
def config_str():
    return """
    [my_table]
    my_key="my_value"
    """


@pytest.fixture
def tmpdirname():
    with TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture
def config_file_path(tmpdirname, config_str):
    config_file_path = os.path.join(tmpdirname, "config.toml")
    with open(config_file_path, "w") as config_file:
        config_file.write(config_str)
    return config_file_path


@pytest.fixture
def config_dict():
    return {"my_table": {"my_key": "my_value"}}


@pytest.fixture(params=["-c", "--config-file"])
def args(request, config_file_path):
    return [request.param, config_file_path]


def test_if_controller_is_stored_as_instance_attribute(toml_cli, controller):
    assert toml_cli.controller is controller


def test_if_parser_error_is_raised_if_invalid_log_level_is_used(capsys, toml_cli, args):
    args += ["--log-file", "my_log_file", "--log-level", "invalid"]
    with pytest.raises(SystemExit):
        toml_cli.clean(args)
    _, err = capsys.readouterr()
    assert err.endswith("Log level invalid is invalid.\n")


def test_if_parser_error_is_raised_if_config_file_can_not_be_found(capsys, config_file_path, toml_cli, args):
    os.remove(config_file_path)
    with pytest.raises(SystemExit):
        toml_cli.clean(args)
    _, err = capsys.readouterr()
    assert err.endswith(f"Could not find configuration file at {config_file_path}.\n")


def test_if_clean_method_of_controller_is_called_correctly(toml_cli, args, controller, config_dict):
    toml_cli.clean(args)
    controller.clean.assert_called_once_with(config_dict)


def test_if_logged_messages_are_correct(caplog, toml_cli, args, config_file_path):
    with caplog.at_level(logging.INFO, logger="dj_cleaner.frameworks.toml_cli"):
        toml_cli.clean(args)
        messages = ["Starting cleaning", f"Loaded TOML configuration file from {config_file_path}", "Finished cleaning"]
        for record, message in zip(caplog.records, messages):
            assert record.message == message


def test_repr(toml_cli):
    assert repr(toml_cli) == "TOMLCLI(controller=controller)"
