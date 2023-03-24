import typing as t
from fastapi import APIRouter, BackgroundTasks, Depends, status
from src.app.customer import schema, service, dependency
from src._base.schema.response import IResponseMessage
from src.app.customer.model import Customer


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(data_in: schema.ICustomerIn):
    return await service.create(data_in=data_in)


@router.get("/me", response_model=schema.ICustomerOut, status_code=status.HTTP_200_OK)
async def get_customer_current_data(
    customer: Customer = Depends(dependency.require_customer),
) -> schema.ICustomerOut:
    return customer


@router.post("/password/reset-link", status_code=status.HTTP_200_OK)
async def reset_password_link(
    customer_data: schema.IGetPasswordResetLink,
) -> IResponseMessage:
    return await service.reset_password_link(customer_data)


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_Customer_email(
    data_in: schema.ICustomerAccountVerifyToken,
) -> IResponseMessage:
    return await service.verify_customer_email(data_in)


@router.put("/password/reset", status_code=status.HTTP_200_OK)
async def update_customer_password(
    data_in: schema.ICustomerResetPassword,
) -> IResponseMessage:
    return await service.update_customer_password(data_in)


@router.put("/password/no_token", status_code=status.HTTP_200_OK)
async def update_customer_password_no_token(
    data_in: schema.ICustomerResetPasswordNoToken,
    user_data: Customer = Depends(dependency.require_customer),
) -> IResponseMessage:
    return await service.update_customer_password_no_token(data_in, user_data)
