from requests_html import HTML

from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaHtml
from tests.conftest import ReadFromTestDataFunc


def test_lamoda_clothing_parse(read_from_test_data: ReadFromTestDataFunc) -> None:
    parse = ParseLamodaHtml()
    html_to_parse = HTML(html=read_from_test_data("lamoda.html"))

    clothing = parse(html_to_parse)
    clothing.images = sorted(clothing.images)

    assert clothing == Clothing(
        title="Mango Man CHERLO",
        type='Футболка',
        images=[
            'https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830316_1_v1.jpg',
            'https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830317_2_v1.jpg',
            'https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830318_3_v1.jpg',
        ]
    )
