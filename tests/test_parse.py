import os

from requests_html import HTML

from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaHtml


def test_lamoda_clothing_parse(test_data_dir: str) -> None:
    parse = ParseLamodaHtml()
    with open(os.path.join(test_data_dir, "lamoda.html"), encoding="utf-8") as f:
        html_to_parse = HTML(html=f.read())

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
