import typing as t
from fastapi import APIRouter, Depends, Request, status
from src.app.auth.schema import ICheckUserEmail, IRefreshToken, IToken
from src.app.users.user import dependency, schema, service
from core.schema.response import IResponseMessage
from src.app.users.user.model import User
from lib.errors import error
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(data_in: schema.IUserIn):
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
    return await service.get_customer(
        user.get("user_id", None), load_related=load_related
    )


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
async def update_users_password_no_token(
    data_in: schema.IUserResetPasswordNoToken,
    user_data: User = Depends(dependency.require_customer),
) -> IResponseMessage:
    return await service.update_users_password_no_token(data_in, user_data)


@router.post(
    "/login",
    response_model=t.Union[IToken, IResponseMessage],
    status_code=status.HTTP_200_OK,
)
async def login(
    request: Request,
    data_in: OAuth2PasswordRequestForm = Depends(),
) -> t.Union[IToken, IResponseMessage]:
    result = await service.login(data_in=data_in, request=request)

    return result


@router.post(
    "/token-refresh",
    response_model=IToken,
    status_code=status.HTTP_200_OK,
)
async def login_token_refresh(data_in: IRefreshToken, request: Request):
    return await service.login_token_refresh(data_in=data_in, request=request)


@router.post(
    "/check/dev", status_code=status.HTTP_200_OK, response_model=IResponseMessage
)
async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    return await service.check_user_email(data_in)
