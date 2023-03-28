import typing as t
import uuid
import pydantic as pyd
from src.app.permission import schema as perm_schema


class IBaseCustomer(pyd.BaseModel):
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


class ICustomerIn(IBaseCustomer):
    password: pyd.SecretStr

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "john@doe.com",
                "password": "****************",
            }
        }


class ICustomerOut(IBaseCustomer):
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
                "email": "john@doe.com",
                "password": "****************",
            }
        }


class ICustomerOutFull(IBaseCustomer):
    id: uuid.UUID
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
                "password": "****************",
            }
        }


class IGetPasswordResetLink(pyd.BaseModel):
    email: pyd.EmailStr


class ICustomerAccountVerifyToken(pyd.BaseModel):
    token: str


class ICustomerResetForgetPassword(pyd.BaseModel):
    email: pyd.EmailStr


class ICustomerRoleUpdate(pyd.BaseModel):
    customer_id: uuid.UUID
    permissions: t.List[uuid.UUID]


class ICustomerRemove(pyd.BaseModel):
    customer_id: uuid.UUID
    permanent: bool = False


class ICustomerResetPassword(pyd.BaseModel):
    token: str
    password: pyd.SecretStr


class ICustomerResetPasswordNoToken(pyd.BaseModel):
    password: pyd.SecretStr
