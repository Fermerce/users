import typing as t
from fastapi import APIRouter, Depends, Query, status
from src.app.market.order import schema, service
from src.app.users.user.model import User
from core.enum.sort_type import SortOrder
from src.app.users.user.dependency import require_customer

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    data_in: schema.IOrderIn, user: User = Depends(require_customer)
):
    return await service.create(data_in=data_in, user=user)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_orders(
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
    user: User = Depends(require_customer),
):
    return await service.get_orders(
        filter=filter,
        select=select,
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        order_by=order_by,
        user=user,
        load_related=load_related,
    )


@router.get("/{order_id}")
async def get_order(order_id: str, user: User = Depends(require_customer)):
    return await service.get_order(order_id=order_id, user=user)


@router.get("/{order_id}/items")
async def get_order_items(order_id: str, user: User = Depends(require_customer)):
    return await service.get_order_items(order_id=order_id, user=user)
