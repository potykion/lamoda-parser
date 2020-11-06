from functools import lru_cache

from fastapi import FastAPI, UploadFile, File, Depends

from src import config
from src.cdn.use_cases import UploadFileToObjectStorage, S3Config
from src.models import LamodaClothing
from src.parse import LamodaClothingParse
from src.utils import get_html_async
from src.view_models import UrlDto

app = FastAPI()


@lru_cache()
def get_config() -> config.Config:
    return config.Config()


@app.get("/")
async def parse(url: str) -> LamodaClothing:
    """Скачивает Lamoda-страничку по {url}, парсит ее, возвращает LamodaClothing"""
    html = await get_html_async(url)
    clothing = LamodaClothingParse(html)()
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
async def upload_image_via_link(image: str):
    ...
