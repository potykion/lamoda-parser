from io import BytesIO
from typing import IO

import httpx
from requests_html import HTML, AsyncHTMLSession, HTMLResponse


class GetHtml:
    """
    Загружает html, выполняя js
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
    """

    async def __call__(self, url: str) -> HTML:
        """Загружает html, выполняя js"""
        session = AsyncHTMLSession()

        resp: HTMLResponse = await session.get(url)
        await resp.html.arender()

        await session.close()

        return resp.html


class GetBinary:
    """Качает файл в бинарном виде"""

    async def __call__(self, url: str) -> IO:
        """Качает файл в бинарном виде"""
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url) as response:
                return BytesIO(await response.aread())
