import typing as t
from fastapi import APIRouter, Depends, Request, status
from src._base.schema.response import IResponseMessage
from src.app.auth.schema import ICheckUserEmail, IRefreshToken, IToken
from src.app.users.staff import schema, service, dependency, model
from src.lib.errors import error
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get(
    "/me",
    response_model=t.Union[schema.IStaffOutFull, schema.IStaffOut],
    status_code=status.HTTP_200_OK,
)
async def get_staff_current_data(
    staff_data: dict = Depends(dependency.AppAuth.authenticate),
    load_related: bool = False,
) -> t.Union[schema.IStaffOutFull, schema.IStaffOut]:
    if not staff_data.get("user_id", None):
        raise error.UnauthorizedError()
    return await service.get_staff(
        staff_id=staff_data.get("user_id", None), load_related=load_related
    )


@router.post("/password/reset-link", status_code=status.HTTP_200_OK)
async def reset_password_link(
    staff_data: schema.IStaffGetPasswordResetLink,
) -> IResponseMessage:
    return await service.reset_password_link(staff_data)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_staff_email(
    data_in: schema.IStaffAccountVerifyToken,
) -> IResponseMessage:
    return await service.verify_staff_email(data_in)


@router.put("/password/reset", status_code=status.HTTP_200_OK)
async def update_staff_password(
    data_in: schema.IStaffResetPassword,
) -> IResponseMessage:
    return await service.update_staff_password(data_in)


@router.put("/password/no_token", status_code=status.HTTP_200_OK)
async def update_staff_password_no_token(
    data_in: schema.IStaffResetPasswordNoToken,
    staff_data: model.Staff = Depends(dependency.require_staff_data_all),
) -> IResponseMessage:
    return await service.update_staff_password_tno_token(data_in, staff_data=staff_data)


@router.post(
    "/login",
    response_model=IToken,
    status_code=status.HTTP_200_OK,
)
async def auth_login(
    request: Request,
    data_in: OAuth2PasswordRequestForm = Depends(),
) -> t.Union[IToken, IResponseMessage]:
    result = await service.login(data_in=data_in, request=request)
    return result


@router.post(
    "/refresh-token",
    response_model=IToken,
    status_code=status.HTTP_200_OK,
)
async def auth_login_token_refresh(data_in: IRefreshToken, request: Request):
    return await service.login_token_refresh(data_in=data_in, request=request)


@router.post(
    "/check/dev", status_code=status.HTTP_200_OK, response_model=IResponseMessage
)
async def check_user_email(data_in: ICheckUserEmail) -> IResponseMessage:
    return await service.check_user_email(data_in)
