import typing as t
import uuid
import pydantic as pyd
from src.app.permission import schema as perm_schema


class IUserOut(pyd.BaseModel):
    id: uuid.UUID
    firstname: str
    lastname: str
    email: pyd.EmailStr
    tel: str
    is_active: t.Optional[bool] = False
    permissions: t.Optional[t.List[perm_schema.IPermissionOut]] = []

    class Config:
        orm_mode = True


class IRegister(pyd.BaseModel):
    firstname: pyd.constr(
        strip_whitespace=True,
        to_lower=True,
        max_length=15,
        min_length=2,
    )
    lastname: pyd.constr(
        strip_whitespace=True,
        to_lower=True,
        max_length=15,
        min_length=2,
    )
    email: pyd.EmailStr
    password: pyd.SecretStr
    tel: pyd.constr(
        regex=r"(\+234|0)?[789]\d{9}",
        strip_whitespace=True,
        min_length=11,
        max_length=14,
        strict=True,
    )

    @pyd.validator("tel")
    def validate_phone_number(cls, v):
        if not v:
            raise ValueError("Phone number is required")
        if len(v) < 11:
            raise ValueError("Phone number must be 11 or 15 digits")
        if len(v) > 14:
            raise ValueError("Phone number must be 11 or 15 digits")
        if not v.startswith(
            (
                "080",
                "081",
                "070",
                "071",
                "090",
                "091",
                "+23480",
                "+23481",
                "+23490",
                "+23491",
                "+23471",
                "+23470",
            )
        ):
            raise ValueError("Invalid Nigerian phone number")
        if not v.startswith(
            ("080", "081", "070", "071", "090", "091", "+23480", "+23481", "+23490")
        ):
            raise ValueError("Invalid Nigerian phone number")
        return v

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
                "tel": "+234567890890",
            }
        }


class IGetPasswordResetLink(pyd.BaseModel):
    email: pyd.EmailStr


class IUserAccountVerifyToken(pyd.BaseModel):
    token: str


class IResetForgetPassword(pyd.BaseModel):
    email: pyd.EmailStr


class IUserPermissionUpdate(pyd.BaseModel):
    permissions: t.List[uuid.UUID]


class IResetPassword(pyd.BaseModel):
    token: str
    password: pyd.SecretStr
