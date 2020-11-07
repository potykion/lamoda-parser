from typing import List

from pydantic import BaseModel


class Clothing(BaseModel):
    """
    Lamoda шмотка

    Пример:
    https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/
    """

    title: str
    type: str
    images: List[str]
    color: str = "ffffff"
