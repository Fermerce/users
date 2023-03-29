import typing as t
from fastapi import APIRouter, Depends, status
from src._base.schema.response import IResponseMessage
from src.app.staff import schema, service, dependency, model
from src.lib.errors import error

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
    if not staff_data.get("staff_id", None):
        raise error.UnauthorizedError()
    return await service.get_staff(
        staff_id=staff_data.get("staff_id", None), load_related=load_related
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
