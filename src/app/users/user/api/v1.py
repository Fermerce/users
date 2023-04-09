import typing as t
from fastapi import APIRouter, Depends, status
from src.app.users.auth.schema import ICheckUserEmail
from src.app.users.user import dependency, schema, service
from core.schema.response import IResponseMessage
from src.app.users.user.model import User
from lib.errors import error


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data_in: schema.IUserIn):
    return await service.create(data_in=data_in)


@router.get(
    "/me",
    response_model=t.Union[schema.IUserOutFull, schema.IUserOut],
    status_code=status.HTTP_200_OK,
)
async def get_users_current_data(
    user: dict = Depends(dependency.AppAuth.authenticate),
    load_related: bool = False,
) -> t.Union[schema.IUserOutFull, schema.IUserOut]:
    if not user.get("user_id", None):
        raise error.UnauthorizedError()
    return await service.get_user(user.get("user_id", None), load_related=load_related)


@router.post("/password/reset-link", status_code=status.HTTP_200_OK)
async def reset_password_link(
    users_data: schema.IGetPasswordResetLink,
) -> IResponseMessage:
    return await service.reset_password_link(users_data)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_User_email(
    data_in: schema.IUserAccountVerifyToken,
) -> IResponseMessage:
    return await service.verify_users_email(data_in)


@router.put("/password/reset", status_code=status.HTTP_200_OK)
async def update_users_password(
    data_in: schema.IUserResetPassword,
) -> IResponseMessage:
    return await service.update_users_password(data_in)


@router.put("/password/no_token", status_code=status.HTTP_200_OK)
async def update_user_password_no_token(
    data_in: schema.IUserResetPasswordNoToken,
    user_data: User = Depends(dependency.require_user),
) -> IResponseMessage:
    return await service.update_users_password_no_token(data_in, user_data)


@router.post(
    "/check/dev", status_code=status.HTTP_200_OK, response_model=IResponseMessage
)
async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    return await service.check_user_email(data_in)
