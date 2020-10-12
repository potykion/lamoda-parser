from typing import cast

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
