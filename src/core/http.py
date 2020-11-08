from io import BytesIO
from typing import io

import httpx
from pydantic import AnyHttpUrl
from requests_html import HTML, AsyncHTMLSession, HTMLResponse


class GetHtml:
    """
    Загружает html, выполняя js
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
    """

    async def __call__(self, url: AnyHttpUrl) -> HTML:
        session = AsyncHTMLSession()

        resp: HTMLResponse = await session.get(url)
        await resp.html.arender()

        await session.close()

        return resp.html


class GetBinary:
    """Качает файл в бинарном виде"""

    async def __call__(self, url: AnyHttpUrl) -> io.IO:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as response:
                return BytesIO(await response.aread())
