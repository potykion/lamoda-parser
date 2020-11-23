from pydantic import BaseModel, AnyHttpUrl


class UrlDto(BaseModel):
    """ДТОшка с урлом"""

    url: AnyHttpUrl


class IdDto(BaseModel):
    """ДТОшка с айди"""
    id: int
