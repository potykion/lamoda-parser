from dataclasses import dataclass
from typing import List, IO

from PIL import Image
from requests_html import HTML

from src.app.config import Config
from src.clothing.db import ClothingRepo
from src.clothing.models import Clothing
from src.core.cdn import UploadFileToObjectStorage
from src.core.http import GetHtml, GetBinary
from src.core.image import search_most_common_color
from src.core.str_ import random_file_name


class ParseLamodaHtml:
    """Парсит хтмл в Ламода шмотку"""

    def __call__(self, html: HTML) -> Clothing:
        """Парсит хтмл в Ламода шмотку"""
        img_tags = html.find("img.x-gallery__image[src$='.jpg']")
        images = sorted({f"https:{t.attrs['src']}" for t in img_tags})

        brand = html.find(".product-title__brand-name", first=True).text
        model = html.find(".product-title__model-name", first=True).text
        type_, title = model.split(" - ")

        title = f"{brand} {title}"

        return Clothing(title=title, type=type_, images=images)


@dataclass()
class ParseLamodaClothing:
    """Парсит Ламода-шмотку"""

    get_html: GetHtml
    get_binary: GetBinary
    parse_lamoda_html: ParseLamodaHtml = ParseLamodaHtml()

    async def __call__(self, url: str) -> Clothing:
        """
        Скачивает хтмл по ссылке на Ламода шмотку, парсит хтмл в шмотку.
        Если есть картинки, то скачивает первую и определяет самый частый цвет.
        """
        html = await self.get_html(url)
        clothing = self.parse_lamoda_html(html)

        if clothing.images:
            image_data = await self.get_binary(clothing.images[0])
            clothing.color = search_most_common_color(Image.open(image_data))

        return clothing


@dataclass()
class CreateClothing:
    """Создание шмотки"""

    config: Config
    get_binary: GetBinary
    upload_file: UploadFileToObjectStorage
    clothing_repo: ClothingRepo

    async def __call__(
        self,
        title: str,
        type: str,
        color: str,
        image_urls: List[str],
        image_files: List[IO],
    ) -> int:
        """Создание шмотки"""
        # загружаем фотки в цдн
        image_files = [
            *image_files,
            *(
                await self.get_binary(url)
                for url in image_urls
                if not url.startswith(self.config.s3_config.endpoint_url)
            ),
        ]
        cdn_image_urls = [
            *(
                url
                for url in image_urls
                if url.startswith(self.config.s3_config.endpoint_url)
            ),
            *(
                await self.upload_file(file, random_file_name("jpg"))
                for file in image_files
            ),
        ]

        # создаем шмотку
        clothing = Clothing(
            title=title,
            type=type,
            images=cdn_image_urls,
            color=color,
        )

        # суем шмотку в бд
        id_ = await self.clothing_repo.insert(clothing)

        # возвращаем айди
        return id_
