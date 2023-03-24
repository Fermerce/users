import typing as t
from fastapi import BackgroundTasks, Request
from fastapi.security.oauth2 import (
    OAuth2PasswordRequestForm,
)
from src.dramatiq_tasks.tasks.user import tasks
from src._base.schema.response import IResponseMessage
from src.lib.errors import error
from src.app.auth import schema
from src.app.auth.repository import auth_token_repo
from src._base.repository.base import BaseRepository, ModelType
from src.lib.utils.cookie_response_token import create_response_cookies
from src.lib.utils.security import JWTAUTH


async def auth_login(
    background_task: BackgroundTasks,
    request: Request,
    data_in: OAuth2PasswordRequestForm,
    user_repo: BaseRepository,
) -> t.Union[schema.IToken, IResponseMessage]:
    check_user: ModelType = await user_repo.get_by_email(email=data_in.username)
    if not check_user:
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.check_password(data_in.password):
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.is_verified:
        tasks.send_activation_email.send(
            dict(email=data_in.email, id=str(check_user.id))
        )
        return IResponseMessage(
            message="Account is not verified, please check your email for verification link"
        )
    else:
        response_data = create_response_cookies(
            user=check_user,
            request=request,
            background_task=background_task,
        )
        if not bool(response_data):
            raise error.ServerError()
        return response_data


async def auth_login_token_refresh(
    data_in: schema.IRefreshToken,
    user_repo: BaseRepository,
    request: Request,
) -> schema.IToken:
    check_auth_token = await auth_token_repo.get_by_attr(
        attr=dict(refresh_token=data_in.refresh_token), first=True
    )
    if not check_auth_token:
        raise error.UnauthorizedError()
    token_data = JWTAUTH.data_decoder(encoded_data=data_in.refresh_token)
    check_user: ModelType = await user_repo.get(token_data.get("user_id", None))
    if check_auth_token.ip_address != auth_token_repo.get_user_ip(request):
        raise error.UnauthorizedError()
    new_token = await auth_token_repo.create(
        user_id=check_user.id,
        request=request,
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
    )
    return schema.IToken(
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
    )


async def check_user_email(
    data_in: schema.ICheckUserEmail,
    user_repo: BaseRepository,
) -> IResponseMessage:
    check_user: ModelType = await user_repo.get_by_email(email=data_in.email)
    if not check_user:
        raise error.NotFoundError()
    return IResponseMessage(message="Account exists")
