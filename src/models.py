from typing import List

from pydantic import BaseModel


class LamodaClothing(BaseModel):
    """
    Lamoda шмотка

    Пример:
    https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/
    """

    title: str
    brand: str
    type: str
    images: List[str]
