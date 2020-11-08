import os
from typing import Callable, Union, io

import pytest


@pytest.fixture()
def root_dir():
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir(root_dir):
    return os.path.join(root_dir, "tests", "data")


ReadFromTestDataFunc = Callable[[str, bool, bool], Union[str, bytes, io.IO]]


@pytest.fixture()
def read_from_test_data(test_data_dir: str) -> ReadFromTestDataFunc:
    def _read(path: str, binary=False, only_file=False):
        read_options = {
            "mode": "rb" if binary else "r",
            "encoding": None if binary else "utf-8"
        }

        if only_file:
            return open(os.path.join(test_data_dir, path), **read_options)
        else:
            with open(os.path.join(test_data_dir, path), **read_options) as input_file:
                return input_file.read()

    return _read
