from functools import lru_cache

from fastapi import Depends

from src.app.config import Config
from src.clothing.use_cases import ParseLamodaClothing
from src.core.cdn import UploadFileToObjectStorage
from src.core.http import GetHtml, GetBinary


@lru_cache()
def get_config() -> Config:
    return Config()


def get_parse_lamoda_clothing(
    get_html: GetHtml = Depends(), get_binary: GetBinary = Depends()
) -> ParseLamodaClothing:
    return ParseLamodaClothing(get_html, get_binary)


def get_upload_file(config: Config = Depends(get_config)) -> UploadFileToObjectStorage:
    return UploadFileToObjectStorage(
        bucket="w2w", dir="images", config=config.s3_config
    )
