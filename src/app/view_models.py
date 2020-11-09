from pydantic import BaseModel, AnyHttpUrl


class UrlDto(BaseModel):
    """ДТОшка с урлом"""

    url: AnyHttpUrl
