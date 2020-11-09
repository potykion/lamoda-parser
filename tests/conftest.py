import os
from typing import Union, Protocol, IO, cast

import pytest
from fastapi.testclient import TestClient

from src.app.app import app
from src.clothing.models import Clothing


@pytest.fixture()
def root_dir() -> str:
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir(root_dir: str) -> str:
    return os.path.join(root_dir, "tests", "data")


class ReadFromTestDataFunc(Protocol):
    def __call__(
        self, path: str, binary: bool = False, only_file: bool = False
    ) -> Union[str, bytes, IO]:
        ...


@pytest.fixture()
def read_from_test_data(test_data_dir: str) -> ReadFromTestDataFunc:
    def _read(
        path: str, binary: bool = False, only_file: bool = False
    ) -> Union[str, bytes, IO]:
        read_options = {
            "mode": "rb" if binary else "r",
            "encoding": None if binary else "utf-8",
        }

        if only_file:
            return cast(IO, open(os.path.join(test_data_dir, path), **read_options))
        else:
            with open(os.path.join(test_data_dir, path), **read_options) as input_file:
                return input_file.read()

    return _read


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def clothing() -> Clothing:
    return Clothing(
        title="Mango Man CHERLO",
        type="Футболка",
        images=[
            "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830316_1_v1.jpg",
            "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830317_2_v1.jpg",
            "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830318_3_v1.jpg",
        ],
    )


@pytest.fixture()
def clothing_with_color(clothing) -> Clothing:
    return clothing.copy(update={"color": "cdb678"})
