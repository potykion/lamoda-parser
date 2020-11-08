from dataclasses import dataclass, asdict
from typing import io

import aioboto3
from pydantic import AnyHttpUrl


@dataclass()
class S3Config:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "ru-central1"
    endpoint_url: str = "https://storage.yandexcloud.net"


@dataclass()
class UploadFileToObjectStorage:
    bucket: str
    dir: str
    config: S3Config

    async def __call__(self, file_like: io.IO, file_name: str) -> AnyHttpUrl:
        async with aioboto3.client("s3", **asdict(self.config)) as s3:
            await s3.upload_fileobj(file_like, self.bucket, f"{self.dir}/{file_name}")

        return f"{self.config.endpoint_url}/{self.bucket}/{self.dir}/{file_name}"

