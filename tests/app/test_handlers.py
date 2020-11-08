from unittest.mock import AsyncMock

from fastapi.testclient import TestClient
from requests_html import HTML

from src.app.app import app
from src.clothing.models import Clothing
from src.core.http import GetHtml, GetBinary
from tests.conftest import ReadFromTestDataFunc

client = TestClient(app)


def test_parse(read_from_test_data: ReadFromTestDataFunc, clothing_with_color: Clothing) -> None:
    app.dependency_overrides[GetHtml] = lambda: AsyncMock(
        return_value=HTML(html=read_from_test_data("lamoda.html"))
    )
    app.dependency_overrides[GetBinary] = lambda: AsyncMock(
        return_value=read_from_test_data("HE002EMKLGV2_11830316_1_v1.jpg", binary=True, only_file=True)
    )

    resp = client.get("/parse", params={"url": "https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/"})

    assert resp.json() == clothing_with_color.dict()


def test_upload_image_via_file(client: TestClient) -> None:
    ...


def test_upload_image_via_link(client: TestClient) -> None:
    ...
