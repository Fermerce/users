import typing as t
import datetime
import uuid
import pydantic as pyd


class IProductPromoCodeIn(pyd.BaseModel):
    code: pyd.constr(max_length=30, min_length=4, strip_whitespace=True)

    class Config:
        schema_extra = {"example": {"code": "12343439klf3"}}


class IProductPromoCodeOut(pyd.BaseModel):
    id: t.Optional[uuid.UUID]
    code: t.Optional[str]
    created_at: t.Optional[datetime.datetime]
    updated_at: t.Optional[datetime.datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12345678-1234-1234-1234-123456789abc",
                "code": "12343439klf3",
                "created_at": "2022-10-25",
                "updated_at": "2022-10-25",
            }
        }
