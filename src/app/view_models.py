from pydantic import BaseModel, AnyHttpUrl


class UrlDto(BaseModel):
    url: AnyHttpUrl
