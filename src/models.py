from dataclasses import dataclass
from typing import List


@dataclass()
class LamodaClothing:
    """
    Lamoda шмотка

    Пример:
    https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/
    """

    title: str
    brand: str
    type: str
    images: List[str]




