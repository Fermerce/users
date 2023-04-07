import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.payment import service, schema
from src.app.user.model import User
from src.base.enum.sort_type import SortOrder
from src.base.schema.response import ResponseMessage
from src.lib.shared.dependency import UserWrite

router = APIRouter(prefix="/payments", tags=["User payments"])


@router.get(
    "/trends",
    status_code=status.HTTP_200_OK,
    response_model=schema.IPaymentTrend,
)
async def get_payment_revenue_trend():
    return await service.get_payment_revenue_trend()


@router.post(
    "/revenue/sum_in_date_range",
    status_code=status.HTTP_200_OK,
    response_model=schema.IPaymentTrend,
)
async def get_revenue_sum_in_date_range(data_in: schema.IPaymentRevenueInDateRange):
    return await service.get_revenue_sum_in_date_range(data_in=data_in)
