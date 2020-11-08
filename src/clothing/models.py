from typing import List

from pydantic import BaseModel, AnyHttpUrl


class Clothing(BaseModel):
    """Шмотка"""

    title: str
    type: str
    images: List[AnyHttpUrl]
    color: str = "ffffff"
