import os

import pytest

from src.core.cdn import UploadFileToObjectStorage, S3Config
from tests.conftest import ReadFromTestDataFunc


@pytest.mark.skip("Коннектится к реальной ЦДНке")
@pytest.mark.asyncio
async def test_upload_file_to_object_storage(read_from_test_data: ReadFromTestDataFunc, ):
    upload_file = UploadFileToObjectStorage(
        bucket="w2w", dir="images",
        config=S3Config(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        )
    )
    test_file = read_from_test_data("kartinka.gif", binary=True, only_file=True)

    url = await upload_file(test_file, "kartinka.gif")
    test_file.close()

    assert url == 'https://storage.yandexcloud.net/w2w/images/kartinka.gif'
