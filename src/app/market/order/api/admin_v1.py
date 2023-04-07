import typing as t
from fastapi import APIRouter, Query, status
from src.app.order import schema, service

from src.base.enum.sort_type import SortOrder


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(
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
    return await service.filter(
        filter=filter,
        page=page,
        per_page=per_page,
        select=select,
        sort_by=sort_by,
        order_by=order_by,
        load_related=load_related,
    )


@router.put("/", status_code=status.HTTP_200_OK)
async def update_order_status(data_in: schema.IOrderUpdate):
    return await service.update_order_status(data_in=data_in)


@router.put("/item", status_code=status.HTTP_200_OK)
async def update_order_item_status(data_in: schema.IOrderItemUpdate):
    return await service.update_order_item_status(data_in=data_in)


@router.delete("/{orderId}")
async def delete_order(orderId: str):
    await service.delete_order(orderId=orderId)
