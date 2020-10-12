from typing import cast

from requests_html import HTMLSession, HTML, HTMLResponse


def get_html(url: str) -> HTML:
    """
    Загружает html, выполняя js
    https://requests.readthedocs.io/projects/requests-html/en/latest/#javascript-support
    """
    session = HTMLSession()
    resp: HTMLResponse = cast(HTMLResponse, session.get(url))
    resp.html.render()
    return resp.html
