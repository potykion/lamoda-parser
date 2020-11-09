from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from requests_html import HTML

from src.app.app import app
from src.app.dependencies import get_upload_file
from src.clothing.models import Clothing
from src.core.http import GetHtml, GetBinary
from tests.conftest import ReadFromTestDataFunc


def test_parse(
    client: TestClient,
    read_from_test_data: ReadFromTestDataFunc,
    clothing_with_color: Clothing,
) -> None:
    """
    Arrange: замоканные скачивание хтмл и скачивание картинки
    Act: кидаем гет-запрос на парс ссылки на шмотку
    Assert: респонс содержит шмотку
    """
    app.dependency_overrides[GetHtml] = lambda: AsyncMock(
        return_value=HTML(html=read_from_test_data("lamoda.html"))
    )
    app.dependency_overrides[GetBinary] = lambda: AsyncMock(
        return_value=read_from_test_data(
            "HE002EMKLGV2_11830316_1_v1.jpg", binary=True, only_file=True
        )
    )

    resp = client.get(
        "/parse",
        params={
            "url": "https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/"
        },
    )

    assert resp.json() == clothing_with_color.dict()


def test_upload_image_via_file(
    client: TestClient, read_from_test_data: ReadFromTestDataFunc
) -> None:
    """
    Arrange: замоканная загрузка картинки в цдн
    Act: кидаем пост-запрос на загрузку картинки через файл
    Assert: в респонсе содержится ссылка на загруженную картинку
    """
    app.dependency_overrides[get_upload_file] = lambda: AsyncMock(
        return_value="https://storage.yandexcloud.net/w2w/images/kartinka.gif"
    )
    image = read_from_test_data("kartinka.gif", binary=True, only_file=True)

    resp = client.post("/upload_image_via_file", files={"image": image})

    assert resp.json() == {
        "url": "https://storage.yandexcloud.net/w2w/images/kartinka.gif"
    }


def test_upload_image_via_link(
    client: TestClient, read_from_test_data: ReadFromTestDataFunc
) -> None:
    """
    Arrange: замоканные скачивание картинки и загрузка картинки в цдн
    Act: кидаем пост-запрос на загрузку картинки через ссылку
    Assert: в респонсе содержится ссылка на загруженную картинку
    """
    app.dependency_overrides[GetBinary] = lambda: AsyncMock(
        return_value=read_from_test_data("kartinka.gif", binary=True)
    )
    app.dependency_overrides[get_upload_file] = lambda: AsyncMock(
        return_value="https://storage.yandexcloud.net/w2w/images/kartinka.gif"
    )

    resp = client.post(
        "/upload_image_via_link",
        json={"url": "https://avatarko.ru/img/kartinka/1/avatarko_anonim.jpg"},
    )

    assert resp.json() == {
        "url": "https://storage.yandexcloud.net/w2w/images/kartinka.gif"
    }
