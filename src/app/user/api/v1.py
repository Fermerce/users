from fastapi import APIRouter, BackgroundTasks, Depends, status
from src.app.user import schema, service
from src.lib.base.schema.response import ResponseMessage
from src.lib.shared.dependency import UserWrite


router = APIRouter(prefix="/users", tags=["Users"], include_in_schema=True)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseMessage)
async def create_user(
    data_in: schema.IRegister,
    background_task: BackgroundTasks,
) -> ResponseMessage:
    return await service.create(background_tasks=background_task, data_in=data_in)


@router.get("/me", response_model=schema.IUserOut, status_code=status.HTTP_200_OK)
async def get_user_current_user_data(
    user_id: str = Depends(UserWrite.current_user),
) -> schema.IUserOut:
    return await service.get_current_user_data(user_id)


@router.post("/password/reset-link", status_code=status.HTTP_200_OK)
async def reset_password_link(
    user_data: schema.IGetPasswordResetLink, background_task: BackgroundTasks
) -> ResponseMessage:
    return await service.reset_password_link(background_task, user_data)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_user_email(
    data_in: schema.IUserAccountVerifyToken,
) -> ResponseMessage:
    return await service.verify_user_email(data_in)


@router.put("/password/reset", status_code=status.HTTP_200_OK)
async def update_user_password(
    data_in: schema.IResetPassword,
) -> ResponseMessage:
    return await service.update_user_password(data_in)
