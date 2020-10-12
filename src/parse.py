from dataclasses import dataclass

from requests_html import HTML

from src.models import LamodaClothing


@dataclass()
class LamodaClothingParse:
    """Парс lamoda-странички со шмоткой"""

    html_to_parse: HTML

    def __call__(self) -> LamodaClothing:
        """Парс lamoda-странички со шмоткой"""
        img_tags = self.html_to_parse.find("img.x-gallery__image[src$='.jpg']")
        images = [*{f"https:{t.attrs['src']}" for t in img_tags}]

        brand = self.html_to_parse.find(".product-title__brand-name", first=True).text
        model = self.html_to_parse.find(".product-title__model-name", first=True).text
        type_, title = model.split(" - ")

        return LamodaClothing(title=title, brand=brand, type=type_, images=images)
