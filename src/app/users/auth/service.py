import typing as t
from fastapi import Request
from lib.exceptions.server_error import ServerError
from lib.exceptions.unauthorize_error import UnauthorizedError
from src.taskiq.auth.tasks import create_token
from core.schema.response import IResponseMessage
from src.app.users.auth import schema
from src.app.users.auth.query import auth_token_query
from lib.utils.security import JWTAUTH


async def auth_login(
    request: Request,
    user_id: str,
) -> t.Union[schema.IToken, IResponseMessage]:
    if not user_id:
        raise ValueError("Invalid data for login request")
    get_jwt_data_for_encode = schema.IToEncode(user_id=str(user_id))
    access_token, refresh_token = JWTAUTH.jwt_encoder(
        data=get_jwt_data_for_encode.dict()
    )
    if access_token and refresh_token:
        user_ip = auth_token_query.get_user_ip(request)
        check_token = await auth_token_query.get_by_attr(
            user_id=str(user_id), user_ip=user_ip
        )
        if check_token:
            await create_token.kiq(
                user_id=str(user_id),
                access_token=access_token,
                refresh_token=refresh_token,
                user_ip=user_ip,
                token_id=check_token.id,
            )
            return schema.IToken(refresh_token=refresh_token, access_token=access_token)
        await create_token.kiq(
            user_id=str(user_id),
            access_token=access_token,
            refresh_token=refresh_token,
            user_ip=user_ip,
        )
        return schema.IToken(refresh_token=refresh_token, access_token=access_token)
    raise ServerError("Count not authenticate user")


async def auth_login_token_refresh(
    data_in: schema.IRefreshToken, request: Request
) -> schema.IToken:
    check_auth_token = await auth_token_query.get_by_attr(
        refresh_token=data_in.refresh_token
    )

    if not check_auth_token:
        raise UnauthorizedError()
    JWTAUTH.data_decoder(encoded_data=data_in.refresh_token)
    user_ip = auth_token_query.get_user_ip(request)
    if check_auth_token.ip_address != user_ip:
        raise UnauthorizedError()
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

    raise ServerError("could not create token, please try again")
