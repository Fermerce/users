import typing as t
from fastapi import Request
from fastapi.security.oauth2 import (
    OAuth2PasswordRequestForm,
)
from src.app.customer.repository import customer_repo
from src.taskiq.auth.tasks import create_token
from src.taskiq.user.tasks import send_customer_activation_email
from src._base.schema.response import IResponseMessage
from src.lib.errors import error
from src.app.auth import schema
from src.app.auth.repository import auth_token_repo
from src._base.repository.base import BaseRepository, ModelType
from src.lib.utils.security import JWTAUTH


async def auth_login(
    request: Request,
    data_in: OAuth2PasswordRequestForm,
    user_repo: BaseRepository = customer_repo,
) -> t.Union[schema.IToken, IResponseMessage]:
    check_user = await user_repo.get_by_email(email=data_in.username)
    if not check_user:
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.check_password(data_in.password):
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.is_verified:
        await send_customer_activation_email.kicker().kiq(
            dict(email=data_in.email, id=str(check_user.id))
        )
        return IResponseMessage(
            message="Account is not verified, please check your email for verification link"
        )
    else:
        get_jwt_data_for_encode = schema.IToEncode(user_id=str(check_user.id))
        access_token, refresh_token = JWTAUTH.jwt_encoder(data=get_jwt_data_for_encode.dict())
        if access_token and refresh_token:
            user_ip = auth_token_repo.get_user_ip(request)
            check_token = await auth_token_repo.get_by_attr(
                attr=dict(user_id=str(check_user.id), user_ip=user_ip), first=True
            )
            if check_token:
                await create_token.kicker().with_labels(delay=5).kiq(
                    user_id=str(check_user.id),
                    access_token=access_token,
                    refresh_token=refresh_token,
                    user_ip=user_ip,
                    token_id=check_token.id,
                )
                return schema.IToken(refresh_token=refresh_token, access_token=access_token)
            await create_token.kicker().with_labels(delay=5).kiq(
                user_id=str(check_user.id),
                access_token=access_token,
                refresh_token=refresh_token,
                user_ip=user_ip,
            )
            return schema.IToken(refresh_token=refresh_token, access_token=access_token)
        raise error.ServerError("Count not authenticate user")


async def auth_login_token_refresh(
    data_in: schema.IRefreshToken,
    request: Request,
    user_repo: BaseRepository = customer_repo,
) -> schema.IToken:
    check_auth_token = await auth_token_repo.get_by_attr(
        attr=dict(refresh_token=data_in.refresh_token), first=True
    )
    if not check_auth_token:
        raise error.UnauthorizedError()
    token_data = JWTAUTH.data_decoder(encoded_data=data_in.refresh_token)
    check_user: ModelType = await user_repo.get(token_data.get("user_id", None))
    user_ip = auth_token_repo.get_user_ip(request)
    if check_auth_token.ip_address != user_ip:
        raise error.UnauthorizedError()

    new_token = await auth_token_repo.create(
        user_id=check_user.id,
        user_ip=user_ip,
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
        return_token=True,
        token_id=check_auth_token.id,
    )
    if new_token:
        return schema.IToken(
            access_token=new_token.access_token,
            refresh_token=new_token.refresh_token,
        )
    raise error.ServerError("could not create token, please try again")


async def check_user_email(
    data_in: schema.ICheckUserEmail,
    user_repo: BaseRepository = customer_repo,
) -> IResponseMessage:
    check_user = await user_repo.get_by_email(email=data_in.email)
    if not check_user:
        raise error.NotFoundError()
    return IResponseMessage(message="Account exists")
