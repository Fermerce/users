import typing as t
import datetime
import uuid
import pydantic as pyd


class IProductMediaIn(pyd.BaseModel):
    alt: str
    url: str
    content_type: str

    class Config:
        schema_extra = {"example": {"name": "Tubber"}}


class IProductMediaOut(pyd.BaseModel):
    id: t.Optional[uuid.UUID]
    alt: str
    url: str
    content_type: str
    created_at: t.Optional[datetime.datetime]
    updated_at: t.Optional[datetime.datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12345678-1234-1234-1234-123456789abc",
                "alt": "photo-update.png",
                "url": "http://example.com/photo-update.png",
                "created_at": "2022-10-25",
                "updated_at": "2022-10-25",
            }
        }
