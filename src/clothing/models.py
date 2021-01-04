from typing import List

from pydantic import AnyHttpUrl
from repka.repositories.base import IdModel


class Clothing(IdModel):
    """Шмотка"""

    title: str
    type: str
    color: str = "ffffff"
    images: List[AnyHttpUrl] = []
