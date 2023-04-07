import typing as t
import datetime
import uuid
import pydantic as pyd


class IProductMeasuringUnitIn(pyd.BaseModel):
    unit: pyd.constr(max_length=30, min_length=2, strip_whitespace=True)

    class Config:
        schema_extra = {"example": {"unit": "kg"}}


class IProductMeasuringUnitOut(pyd.BaseModel):
    id: t.Optional[uuid.UUID]
    unit: t.Optional[str]
    created_at: t.Optional[datetime.datetime]
    updated_at: t.Optional[datetime.datetime]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "12345678-1234-1234-1234-123456789abc",
                "unit": "edit_product",
                "created_at": "2022-10-25",
                "updated_at": "2022-10-25",
            }
        }
