import typing as t
import datetime
import uuid
import pydantic as pyd


class IProductPromoCodeIn(pyd.BaseModel):
    code: pyd.constr(max_length=25, min_length=4, strip_whitespace=True)
    discount: t.Optional[float] = 0.0
    start: t.Optional[datetime.datetime] = datetime.datetime.utcnow()
    end: t.Optional[
        datetime.datetime
    ] = datetime.datetime.utcnow() + datetime.timedelta(days=10)

    class Config:
        schema_extra = {"example": {"code": "12343439klf3"}}


class IProductPromoCodeOut(IProductPromoCodeIn):
    id: t.Optional[uuid.UUID]
    pass

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12345678-1234-1234-1234-123456789abc",
                "code": "12343439klf3",
                "discount": 10.0,
                "start": "12345678-1234-1234",
                "end": "12345678-1234-1234",
                "created_at": "2022-10-25",
                "updated_at": "2022-10-25",
            }
        }
