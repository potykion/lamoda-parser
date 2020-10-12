from fastapi import FastAPI

from src.models import LamodaClothing
from src.parse import LamodaClothingParse
from src.utils import get_html_async

app = FastAPI()


@app.get("/")
async def parse(url: str) -> LamodaClothing:
    """Скачивает Lamoda-страничку по {url}, парсит ее, возвращает LamodaClothing"""
    html = await get_html_async(url)
    clothing = LamodaClothingParse(html)()
    return clothing
