from typing import List

from pydantic import BaseModel


class Clothing(BaseModel):
    """Шмотка"""

    title: str
    type: str
    images: List[str]
    color: str = "ffffff"
