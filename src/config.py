from pydantic import BaseSettings

from src.cdn.use_cases import S3Config


class Config(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = ".env"

    @property
    def s3_config(self) -> S3Config:
        return S3Config(
            self.aws_access_key_id,
            self.aws_secret_access_key,
        )
