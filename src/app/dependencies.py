from functools import lru_cache

from aiopg.sa import SAConnection
from fastapi import Depends

from src.app.config import Config
from src.app.meta import db_var
from src.clothing.db import ClothingRepo
from src.clothing.use_cases import ParseLamodaClothing, CreateClothing
from src.core.cdn import UploadFileToObjectStorage
from src.core.http import GetHtml, GetBinary


@lru_cache()
def get_config() -> Config:
    """Зависимость конфига"""
    return Config()


def get_parse_lamoda_clothing(
    get_html: GetHtml = Depends(), get_binary: GetBinary = Depends()
) -> ParseLamodaClothing:
    """Зависимость парса ссылки в Ламода шмотку"""
    return ParseLamodaClothing(get_html, get_binary)


def get_upload_file(config: Config = Depends(get_config)) -> UploadFileToObjectStorage:
    """Зависимость загрузки файла в цдн"""
    return UploadFileToObjectStorage(
        bucket="w2w", dir="images", config=config.s3_config
    )


async def get_connection() -> SAConnection:
    """Создает соединение к бд"""
    async with db_var.get().acquire() as conn:
        yield conn


def get_clothing_repo(
    connection: SAConnection = Depends(get_connection),
) -> ClothingRepo:
    """Зависимость репо для работы со шмотками"""
    return ClothingRepo(connection)


def get_create_clothing(
    config: Config = Depends(get_config),
    get_binary: GetBinary = Depends(),
    upload_file: UploadFileToObjectStorage = Depends(get_upload_file),
    clothing_repo: ClothingRepo = Depends(get_clothing_repo),
) -> CreateClothing:
    """Зависимость создания шмотки"""
    return CreateClothing(config, get_binary, upload_file, clothing_repo)
