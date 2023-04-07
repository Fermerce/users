import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.payment import service, schema
from src.app.user.model import User
from src.base.enum.sort_type import SortOrder
from src.base.schema.response import ResponseMessage
from src.lib.shared.dependency import UserWrite

router = APIRouter(prefix="/payments", tags=["User payments"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schema.IPaymentInitOut
)
async def create_payment_link(
    data_in: schema.IPaymentIn, user: User = Depends(UserWrite.current_user_with_data)
):
    return await service.create_payment(data_in=data_in, user=user)


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=t.List[schema.IPaymentOrderOut]
)
async def get_payment_list(
    user: User = Depends(UserWrite.current_user_with_data),
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all shipping_address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the permissions",
    ),
    per_page: int = 10,
    page: int = 1,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id", description="order by attribute, e.g. id"
    ),
    load_related: bool = False,
):
    return await service.payment_list(
        select=select,
        filter=filter,
        user=user,
        per_page=per_page,
        page=page,
        sort_by=sort_by,
        order_by=order_by,
        load_related=load_related,
    )


@router.get(
    "/{payment_id}",
    status_code=status.HTTP_200_OK,
    response_model=schema.IPaymentOrderOut,
)
async def get_payment_by_id(
    payment_id: uuid.UUID, user: User = Depends(UserWrite.current_user_with_data)
):
    return await service.get_payment(payment_id, user)


@router.put("/", status_code=status.HTTP_200_OK, response_model=ResponseMessage)
async def verify_payment(
    data_in: schema.IVerifyPaymentResponse,
    user: User = Depends(UserWrite.current_user_with_data),
):
    return await service.verify_user_payment(data_in=data_in, user=user)
