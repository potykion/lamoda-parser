from fastapi import UploadFile, File, Depends, APIRouter
from pydantic import AnyHttpUrl

from src.app.dependencies import get_parse_lamoda_clothing, get_upload_file
from src.app.view_models import UrlDto
from src.clothing.models import Clothing
from src.clothing.use_cases import ParseLamodaClothing
from src.core.cdn import UploadFileToObjectStorage
from src.core.http import GetBinary
from src.core.str_ import random_file_name

router = APIRouter()


@router.get("/parse", response_model=Clothing)
async def parse(
    url: AnyHttpUrl,
    parse_lamoda_clothing: ParseLamodaClothing = Depends(get_parse_lamoda_clothing),
) -> Clothing:
    """Скачивает Lamoda-страничку по {url}, парсит ее, возвращает LamodaClothing"""
    clothing = await parse_lamoda_clothing(url)
    return clothing


@router.post("/upload_image_via_file", response_model=UrlDto)
async def upload_image_via_file(
    image: UploadFile = File(...),
    upload_file: UploadFileToObjectStorage = Depends(get_upload_file),
) -> UrlDto:
    url = await upload_file(image.file, image.filename)

    return UrlDto(url=url)


@router.post("/upload_image_via_link", response_model=UrlDto)
async def upload_image_via_link(
    image_url: UrlDto,
    upload_file: UploadFileToObjectStorage = Depends(get_upload_file),
    get_binary: GetBinary = Depends(),
) -> UrlDto:
    url = await upload_file(
        file_like=await get_binary(image_url.url), file_name=random_file_name()
    )

    return UrlDto(url=url)
