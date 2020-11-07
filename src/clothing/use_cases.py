from dataclasses import dataclass

from PIL import Image
from requests_html import HTML

from src.clothing.models import Clothing
from src.core.http import GetHtml, GetBinary
from src.core.image import search_most_common_color


class ParseLamodaHtml:
    def __call__(self, html: HTML) -> Clothing:
        img_tags = html.find("img.x-gallery__image[src$='.jpg']")
        images = [*{f"https:{t.attrs['src']}" for t in img_tags}]

        brand = html.find(".product-title__brand-name", first=True).text
        model = html.find(".product-title__model-name", first=True).text
        type_, title = model.split(" - ")

        title = f"{brand} {title}"

        return Clothing(title=title, type=type_, images=images)


@dataclass()
class ParseLamodaClothing:
    get_html: GetHtml
    get_binary: GetBinary
    parse_lamoda_html: ParseLamodaHtml = ParseLamodaHtml()

    async def __call__(self, url: str) -> Clothing:
        html = await self.get_html(url)
        clothing = self.parse_lamoda_html(html)

        if clothing.images:
            image_data = await self.get_binary(clothing.images[0])
            clothing.color = search_most_common_color(Image.open(image_data))

        return clothing
