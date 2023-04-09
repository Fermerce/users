import typing as t
from fastapi import Request
from core.enum.sort_type import SearchType
from src.taskiq.auth.tasks import create_token
from core.schema.response import IResponseMessage
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.app.users.user.repository import users_repo
from lib.errors import error
from src.app.auth import schema
from src.app.users.auth.repository import auth_token_repo
from lib.utils.security import JWTAUTH
from src.taskiq.user import tasks


async def login(
    request: Request, data_in: OAuth2PasswordRequestForm
) -> t.Union[schema.IToken, IResponseMessage]:
    check_user = await users_repo.get_by_attr(
        attr=dict(username=data_in.username, email=data_in.username),
        first=True,
        search_mode=SearchType._or,
    )
    if not check_user:
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.check_password(data_in.password):
        raise error.UnauthorizedError(detail="incorrect email or password")
    if not check_user.is_verified:
        await tasks.send_users_activation_email.kiq(
            dict(email=data_in.username, id=str(check_user.id))
        )
        return IResponseMessage(
            message="Your is not verified, Please check your for verification link before continuing"
        )

    get_jwt_data_for_encode = schema.IToEncode(user_id=str(check_user.id))
    access_token, refresh_token = JWTAUTH.jwt_encoder(
        data=get_jwt_data_for_encode.dict()
    )
    if access_token and refresh_token:
        user_ip = auth_token_repo.get_user_ip(request)
        check_token = await auth_token_repo.get_by_attr(
            user_id=str(check_user.id), user_ip=user_ip
        )
        if check_token:
            await create_token.kiq(
                user_id=str(check_user.id),
                access_token=access_token,
                refresh_token=refresh_token,
                user_ip=user_ip,
                token_id=check_token.id,
            )
            return schema.IToken(refresh_token=refresh_token, access_token=access_token)
        await create_token.kiq(
            user_id=str(check_user.id),
            access_token=access_token,
            refresh_token=refresh_token,
            user_ip=user_ip,
        )
        return schema.IToken(refresh_token=refresh_token, access_token=access_token)
    raise error.ServerError("Count not authenticate user")


async def login_token_refresh(
    data_in: schema.IRefreshToken, request: Request
) -> schema.IToken:
    check_auth_token = await auth_token_repo.get_by_attr(
        refresh_token=data_in.refresh_token
    )

    if not check_auth_token:
        raise error.UnauthorizedError()
    JWTAUTH.data_decoder(encoded_data=data_in.refresh_token)
    user_ip = auth_token_repo.get_user_ip(request)
    if check_auth_token.ip_address != user_ip:
        raise error.UnauthorizedError()
    get_jwt_data_for_encode = schema.IToEncode(user_id=str(check_auth_token.user_id))
    access_token, refresh_token = JWTAUTH.jwt_encoder(
        data=get_jwt_data_for_encode.dict()
    )
    if access_token and refresh_token:
        await create_token.kiq(
            user_id=str(check_auth_token.user_id),
            user_ip=user_ip,
            access_token=access_token,
            refresh_token=refresh_token,
            token_id=str(check_auth_token.id),
        )
        return schema.IToken(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    raise error.ServerError("could not create token, please try again")
