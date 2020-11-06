import uuid
from io import BytesIO
from typing import cast, io, Tuple

import httpx
from requests_html import HTMLSession, HTML, HTMLResponse, AsyncHTMLSession


def get_html(url: str) -> HTML:
    """
    Загружает html, выполняя js
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
    """
    session = HTMLSession()
    resp: HTMLResponse = cast(HTMLResponse, session.get(url))
    resp.html.render()
    return resp.html


async def get_html_async(url: str) -> HTML:
    """
    Асинхронно загружает html, выполняя js
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
    """
    session = AsyncHTMLSession()
    resp: HTMLResponse = await session.get(url)
    await resp.html.arender()
    return resp.html


def random_file_name(extension: str = "jpg") -> str:
    """
    >>> random_file_name("png").endswith(".png")
    True
    """
    file_name = str(uuid.uuid4().hex)
    return f"{file_name}.{extension}"


async def download_image_file(url: str, file_name: str = None) -> Tuple[io.IO, str]:
    """Асинхронно качает картинку"""
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', url) as response:
            file_data = BytesIO(await response.aread())
            file_name = file_name or random_file_name()
            return file_data, file_name
