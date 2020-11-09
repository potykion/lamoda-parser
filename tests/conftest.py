import os
from typing import Union, Protocol, IO

import pytest
from fastapi.testclient import TestClient

from src.app.app import app
from src.clothing.models import Clothing


@pytest.fixture()
def root_dir() -> str:
    """Директория проекта"""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture()
def test_data_dir(root_dir: str) -> str:
    """Директория с тестовыми данными"""
    return os.path.join(root_dir, "tests", "data")


class ReadFromTestDataFunc(Protocol):
    """Функция для чтения файла из директории с тестовыми данными"""

    def __call__(
        self, path: str, binary: bool = False, only_file: bool = False
    ) -> Union[str, bytes, IO]:
        """
        Функция для чтения файла из директории с тестовыми данными
        :param path: путь к файлу в директории с тестовыми данными
        :param binary: True - возвращает содержимое файла в байтах, False - в виде строки
        :param only_file: True - возвращает file-like объект, из которого можно читать данные
        """
        ...


@pytest.fixture()
def read_from_test_data(test_data_dir: str) -> ReadFromTestDataFunc:
    """Функция для чтения файла из директории с тестовыми данными"""

    def _read(
        path: str, binary: bool = False, only_file: bool = False
    ) -> Union[str, bytes, IO]:
        open_ = open(
            os.path.join(test_data_dir, path),
            mode="rb" if binary else "r",
            encoding=None if binary else "utf-8",
        )

        if only_file:
            return open_
        else:
            with open_ as input_file:
                return input_file.read()

    return _read


@pytest.fixture()
def client() -> TestClient:
    """Штука для тестирования серва"""
    return TestClient(app)


@pytest.fixture()
def clothing() -> Clothing:
    """Шмотка"""
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
def clothing_with_color(clothing: Clothing) -> Clothing:
    """Щмотка с цветом"""
    return clothing.copy(update={"color": "cdb678"})
