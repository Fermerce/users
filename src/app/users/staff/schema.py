import re
import typing as t
import uuid
import pydantic as pyd
from src.app.users.permission import schema as perm_schema


class IStaffIn(pyd.BaseModel):
    user_id = uuid.UUID

    class Config:
        schema_extra = {"example": {"user_id": uuid.UUID}}


class IStaffOut(pyd.BaseModel):
    id: uuid.UUID
    tel: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "firstname": "John",
                "aud": "st-vguytt",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
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


class IStaffOutFull(pyd.BaseModel):
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
