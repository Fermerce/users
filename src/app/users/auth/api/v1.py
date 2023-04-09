import typing as t
from fastapi import APIRouter, Depends, Request, status
from src.app.users.auth.schema import IRefreshToken, IToken
from src.app.users.user import service
from core.schema.response import IResponseMessage
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])


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
