import typing as t
import uuid
import pydantic as pyd
from src.app.users.permission import schema as perm_schema


class IBaseUser(pyd.BaseModel):
    firstname: t.Optional[
        pyd.constr(
            strip_whitespace=True,
            to_lower=True,
            max_length=15,
            min_length=2,
        )
    ]
    lastname: t.Optional[
        pyd.constr(
            strip_whitespace=True,
            to_lower=True,
            max_length=15,
            min_length=2,
        )
    ]
    email: pyd.EmailStr
    username: str


class IUserIn(IBaseUser):
    username: str
    email: pyd.EmailStr
    password: pyd.SecretStr

    class Config:
        schema_extra = {
            "example": {
                "username": {"required": False, "example": "jonD"},
                "email": "john@doe.com",
                "password": "****************",
            }
        }


class IUserUpdateIn(IBaseUser):
    id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "id": str(uuid.uuid4()),
                "firstname": {"required": False, "example": "John"},
                "lastname": {"required": False, "example": "doe"},
                "username": {"required": False, "example": "jonD"},
                "email": "john@doe.com",
            }
        }


class IUserOut(IBaseUser):
    id: uuid.UUID
    is_active: t.Optional[bool] = False
    is_suspended: t.Optional[bool] = False
    is_verified: t.Optional[bool] = False

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "2345678-1234-1234-1234-123456789abc",
                "firstname": "John",
                "lastname": "Doe",
                "username": "JonD",
                "email": "john@doe.com",
                "password": "****************",
            }
        }


class IUserOutFull(IBaseUser):
    email: t.Optional[pyd.EmailStr]
    username: t.Optional[str]
    id: t.Optional[uuid.UUID]
    is_active: t.Optional[bool] = False
    is_suspended: t.Optional[bool] = False
    is_verified: t.Optional[bool] = False
    permissions: t.Optional[t.List[perm_schema.IPermissionOut]] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "2345678-1234-1234-1234-123456789abc",
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
            }
        }


class IGetPasswordResetLink(pyd.BaseModel):
    email: pyd.EmailStr


class IUserAccountVerifyToken(pyd.BaseModel):
    token: str


class IUserResetForgetPassword(pyd.BaseModel):
    email: pyd.EmailStr


class IUserRoleUpdate(pyd.BaseModel):
    users_id: uuid.UUID
    permissions: t.List[uuid.UUID]


class IUserRemove(pyd.BaseModel):
    users_id: uuid.UUID
    permanent: bool = False


class IUserResetPassword(pyd.BaseModel):
    token: str
    password: pyd.SecretStr


class IUserResetPasswordNoToken(pyd.BaseModel):
    password: pyd.SecretStr
    old_password: pyd.SecretStr
