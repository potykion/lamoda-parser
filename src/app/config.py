from pydantic import BaseSettings

from src.core.cdn import S3Config


class Config(BaseSettings):
    """Конфиг приложения, парсится из .env файла"""

    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = ".env"

    @property
    def s3_config(self) -> S3Config:
        """Конфиг для Yandex Object Storage (аналог amazon s3)"""
        return S3Config(
            self.aws_access_key_id,
            self.aws_secret_access_key,
        )
