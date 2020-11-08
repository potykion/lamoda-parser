from functools import lru_cache

from fastapi import Depends

from src.app.config import Config
from src.clothing.use_cases import ParseLamodaClothing
from src.core.cdn import S3Config, UploadFileToObjectStorage
from src.core.http import GetHtml, GetBinary


@lru_cache()
def get_config() -> Config:
    return Config()


@lru_cache()
def get_s3_config(config_: Config = Depends(get_config)) -> S3Config:
    return config_.s3_config


def get_get_html() -> GetHtml:
    return GetHtml()


def get_get_binary() -> GetBinary():
    return GetBinary()


def get_parse_lamoda_clothing(
    get_html: GetHtml = Depends(get_get_html),
    get_binary: GetBinary = Depends(get_get_binary)
) -> ParseLamodaClothing:
    return ParseLamodaClothing(get_html, get_binary)


@lru_cache()
def get_upload_file(
    s3_config: S3Config = Depends(get_s3_config)
) -> UploadFileToObjectStorage:
    return UploadFileToObjectStorage(
        bucket="w2w",
        dir="images",
        config=s3_config
    )
