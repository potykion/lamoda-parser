import binascii
import uuid
from io import BytesIO
from typing import cast, io, Tuple

import httpx
import numpy as np
import scipy
from PIL import Image
from numpy import random
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


def image_from_file(file_data: io.IO) -> Image.Image:
    return Image.open(file_data)


def search_most_common_color(image: Image.Image) -> str:
    """
    Ищет самый частый цвет в картинке

    Ставит сид, чтобы одинаковые результаты были
    Вырезает серединку, чтобы игнорить фон и бошку
    Затем по алгоритму:
    https://stackoverflow.com/a/3244061
    """
    random.seed((1000, 2000))

    cropped = image.crop((
        image.width / 3,
        image.height / 3,
        image.width * 2 / 3,
        image.height * 2 / 3
    ))

    ar = np.asarray(cropped)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    codes, dist = scipy.cluster.vq.kmeans(ar, 5, )
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    return color
