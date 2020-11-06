from dataclasses import dataclass

from requests_html import HTML

from src.models import Clothing
from src.utils import get_html_async, download_image_file, image_from_file, search_most_common_color


class _LamodaClothingHTMLParser:
    """Парс lamoda-странички со шмоткой"""

    def __call__(self, html_to_parse: HTML) -> Clothing:
        """Парс lamoda-странички со шмоткой"""
        img_tags = html_to_parse.find("img.x-gallery__image[src$='.jpg']")
        images = [*{f"https:{t.attrs['src']}" for t in img_tags}]

        brand = html_to_parse.find(".product-title__brand-name", first=True).text
        model = html_to_parse.find(".product-title__model-name", first=True).text
        type_, title = model.split(" - ")

        return Clothing(title=title, brand=brand, type=type_, images=images)


@dataclass()
class ParseLamodaClothing:
    parser: _LamodaClothingHTMLParser

    async def __call__(self, url: str) -> Clothing:
        html = await get_html_async(url)

        clothing = self.parser(html)

        if clothing.images:
            image_url = clothing.images[0]
            image_data, image_name = await download_image_file(image_url)
            image = image_from_file(image_data)
            clothing.color = search_most_common_color(image)

        return clothing
