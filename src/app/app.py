from functools import lru_cache

from fastapi import FastAPI, UploadFile, File, Depends

from src.core.http import GetHtml, GetBinary
from src.core.str_ import random_file_name
from src.app import config
from src.core.cdn import UploadFileToObjectStorage
from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaClothing
from src.app.view_models import UrlDto

app = FastAPI()


@lru_cache()
def get_config() -> config.Config:
    return config.Config()


@app.get("/")
async def parse(url: str) -> Clothing:
    """Скачивает Lamoda-страничку по {url}, парсит ее, возвращает LamodaClothing"""
    clothing = await ParseLamodaClothing(GetHtml(), GetBinary())(url)
    return clothing


@app.post("/upload_image_via_file")
async def upload_image_via_file(image: UploadFile = File(...), config_: config.Config = Depends(get_config)) -> UrlDto:
    # todo сделать как зависимость
    upload_file = UploadFileToObjectStorage(
        bucket="w2w", dir="images",
        config=config_.s3_config
    )

    url = await upload_file(image.file, image.filename)

    return UrlDto(url=url)


@app.post("/upload_image_via_link")
async def upload_image_via_link(image_url: str, config_: config.Config = Depends(get_config)) -> UrlDto:
    upload_file = UploadFileToObjectStorage(
        bucket="w2w", dir="images",
        config=config_.s3_config
    )
    get_binary = GetBinary()

    url = await upload_file(
        file_like=await get_binary(image_url),
        file_name=random_file_name()
    )

    return UrlDto(url=url)
