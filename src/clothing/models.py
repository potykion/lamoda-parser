from typing import List

from pydantic import AnyHttpUrl
from repka.repositories.base import IdModel


class Clothing(IdModel):
    """Шмотка"""

    title: str
    type: str
    images: List[AnyHttpUrl]
    color: str = "ffffff"
