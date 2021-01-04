from typing import cast
from unittest.mock import AsyncMock

import pytest
from requests_html import HTML

from src.app.config import Config
from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaHtml, ParseLamodaClothing, CreateClothing
from tests.conftest import ReadFromTestDataFunc


def test_parse_lamoda_html(
    read_from_test_data: ReadFromTestDataFunc, clothing: Clothing
) -> None:
    """
    Arrange: html для парса
    Act: парсим html в шмотку
    Assert: распаршеная шмотка = ожидаемой
    """
    html_to_parse = HTML(html=read_from_test_data("lamoda.html"))

    actual_clothing = ParseLamodaHtml()(html_to_parse)

    assert actual_clothing == clothing


@pytest.mark.asyncio
async def test_parse_lamoda_clothing(
    read_from_test_data: ReadFromTestDataFunc, clothing_with_color: Clothing
) -> None:
    """
    Arrange: Функция парса ламода-шмотки с моками
    Act: Вызываем парс
    Assert: Распаршенная шмотка = ожидаемой
    """
    parse = ParseLamodaClothing(
        get_html=AsyncMock(return_value=HTML(html=read_from_test_data("lamoda.html"))),
        get_binary=AsyncMock(
            return_value=read_from_test_data(
                "HE002EMKLGV2_11830316_1_v1.jpg", binary=True, only_file=True
            )
        ),
    )

    actual_clothing = await parse(
        "https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/"
    )

    assert actual_clothing == clothing_with_color

@pytest.mark.asyncio
async def test_create_clothing():
    create_clothing = CreateClothing(
        config=Config(db_url=""),
        get_binary=AsyncMock(),
        upload_file=AsyncMock(),
        clothing_repo=AsyncMock()
    )
    clothing = await create_clothing(
        title="mango man",
        type="shirt",
        color="ff0000",
        image_urls=[],
        image_files=[],
    )

    assert clothing == Clothing(
        title="mango man",
        type="shirt",
        color="ff0000",
    )
    cast(AsyncMock, create_clothing.clothing_repo.insert).assert_awaited()
