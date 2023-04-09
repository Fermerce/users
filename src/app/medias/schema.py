import typing as t
import pydantic as pyd


class IMedia(pyd.BaseModel):
    alt: str
    url: pyd.AnyUrl
    content_type: str


class IMediaOut(pyd.BaseModel):
    alt: str
    url: pyd.AnyUrl
    content_type: str

    class Config:
        orm_mode = True


class IMediaDeleteIn(pyd.BaseModel):
    uris: t.List[str] = []
    trash = False
