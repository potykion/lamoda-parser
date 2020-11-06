import asyncio
import os
from dataclasses import dataclass, asdict
from typing import io

import aioboto3


@dataclass()
class S3Config:
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "ru-central1"
    endpoint_url = "https://storage.yandexcloud.net"


@dataclass()
class UploadFileToObjectStorage:
    bucket: str
    dir: str
    config: S3Config

    async def __call__(self, file_like: io.IO, file_name: str) -> str:
        async with aioboto3.client("s3", **asdict(self.config)) as s3:
            await s3.upload_fileobj(file_like, self.bucket, f"{self.dir}/{file_name}")

        return f"{self.config.endpoint_url}/{self.bucket}/{self.dir}/{file_name}"


async def main():
    upload_file = UploadFileToObjectStorage(
        bucket="w2w", dir="images",
        config=S3Config(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
    )
    with open("test_data/kartinka.gif", "rb") as f:
        url = await upload_file(f, "kartinka.gif")
    print(url)


if __name__ == '__main__':
    asyncio.run(main())
