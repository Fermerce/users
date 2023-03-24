from fastapi import APIRouter, BackgroundTasks, Depends, status
from src.app.staff import schema, service, model
from src._base.schema.response import IResponseMessage
from src.app.staff import schema, service, dependency

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("/me", response_model=schema.IStaffOut, status_code=status.HTTP_200_OK)
async def get_staff_current_data(
    staff_data: model.Staff = Depends(dependency.require_staff_data_all),
) -> schema.IStaffOut:
    return staff_data


@router.post("/password/reset-link", status_code=status.HTTP_200_OK)
async def reset_password_link(
    staff_data: schema.IStaffGetPasswordResetLink, background_task: BackgroundTasks
) -> IResponseMessage:
    return await service.reset_password_link(background_task, staff_data)


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
