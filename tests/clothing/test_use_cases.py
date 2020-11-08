from unittest.mock import AsyncMock

import pytest
from requests_html import HTML

from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaHtml, ParseLamodaClothing
from tests.conftest import ReadFromTestDataFunc


def test_parse_lamoda_html(read_from_test_data: ReadFromTestDataFunc, clothing: Clothing) -> None:
    parse = ParseLamodaHtml()
    html_to_parse = HTML(html=read_from_test_data("lamoda.html"))

    actual_clothing = parse(html_to_parse)

    assert actual_clothing == clothing


@pytest.mark.asyncio
async def test_parse_lamoda_clothing(read_from_test_data: ReadFromTestDataFunc, clothing_with_color: Clothing) -> None:
    parse = ParseLamodaClothing(
        get_html=AsyncMock(return_value=HTML(html=read_from_test_data("lamoda.html"))),
        get_binary=AsyncMock(
            return_value=read_from_test_data("HE002EMKLGV2_11830316_1_v1.jpg", binary=True, only_file=True)),
    )

    actual_clothing = await parse("https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/")

    assert actual_clothing == clothing_with_color
