import typing as t
import datetime
import uuid
import pydantic as pyd


class IPermissionIn(pyd.BaseModel):
    name: pyd.constr(max_length=30, min_length=4, strip_whitespace=True)


class IPermissionOut(pyd.BaseModel):
    id: t.Optional[uuid.UUID]
    name: t.Optional[str]
    created_at: t.Optional[datetime.datetime]
    updated_at: t.Optional[datetime.datetime]

    class Config:
        orm_mode = True
