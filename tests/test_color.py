import pytest
import requests
from PIL import Image

from src.core.image import search_most_common_color


@pytest.mark.parametrize(
    "url, color",
    [
        ("https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830316_1_v1.jpg", 'e3cfa0'),
        ("https://a.lmcdn.ru/img600x866/T/R/TR776EMKFNC4_11819445_1_v1_2x.jpg", '73565d')

    ]
)
def test_most_common_color_search(url: str, color: str) -> None:
    img = Image.open(requests.get(url, stream=True).raw)
    assert search_most_common_color(img) == color
