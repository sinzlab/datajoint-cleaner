from unittest.mock import MagicMock

import pytest


@pytest.fixture
def config():
    return MagicMock(name="config")
