import re
import typing as t
import uuid
import pydantic as pyd
from src.app.permission import schema as perm_schema


class IBaseStaff(pyd.BaseModel):
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


class IStaffIn(IBaseStaff):
    password: pyd.SecretStr
    tel: pyd.constr(
        strip_whitespace=True,
        min_length=11,
        max_length=14,
        strict=True,
    )

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
                "tel": "08089223577",
            }
        }

    @pyd.validator("tel", pre=True)
    def validate_phone_number(cls, v):
        phone_number_regex = r"^\+?234(7[01]|8[01]|9[01])\d{8}$"
        if not v:
            raise ValueError("Phone number is required")
        if not re.match(phone_number_regex, v):
            raise ValueError("Phone number must be 11 or 15 digits")
        if v.startswith("234"):
            v = f"+{v}"
        return v


class IStaffOut(IBaseStaff):
    id: uuid.UUID
    tel: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
                "tel": "08089223577 or +234",
                "permissions": [
                    {
                        "name": "admin",
                    }
                ],
                "is_active": True,
                "is_suspected": True,
                "is_verified": True,
            }
        }


class IStaffOutFull(IBaseStaff):
    id: uuid.UUID
    tel: str
    permissions: t.Optional[t.List[perm_schema.IPermissionOut]] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
                "tel": "08089223577 or +234",
                "permissions": [
                    {
                        "name": "admin",
                    }
                ],
                "is_active": True,
                "is_suspected": True,
                "is_verified": True,
            }
        }


class IStaffGetPasswordResetLink(pyd.BaseModel):
    email: pyd.EmailStr


class IStaffAccountVerifyToken(pyd.BaseModel):
    token: str


class IStaffResetForgetPassword(pyd.BaseModel):
    email: pyd.EmailStr


class IStaffRoleUpdate(pyd.BaseModel):
    staff_id: str
    permissions: t.List[uuid.UUID]


class IRemoveStaff(pyd.BaseModel):
    staff_id: str
    permanent: bool = False


class IStaffResetPassword(pyd.BaseModel):
    token: str
    password: pyd.SecretStr


class IStaffResetPasswordNoToken(pyd.BaseModel):
    password: pyd.SecretStr
