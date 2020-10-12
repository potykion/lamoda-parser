import os

import pytest


@pytest.fixture()
def root_dir():
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir(root_dir):
    return os.path.join(root_dir, "tests", "data")
