import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status

from src.app.cart import schema, service
from src.app.user.model import User
from src.base.enum.sort_type import SortOrder
from src.lib.shared.dependency import UserWrite

router = APIRouter(prefix="/carts", tags=["Carts"], include_in_schema=True)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cart(
    data_in: schema.ICartIn, user: User = Depends(UserWrite.current_user_with_data)
):
    return await service.create(data_in, user)


@router.put("/{cart_id}", status_code=status.HTTP_200_OK)
async def update_cart(
    cart_id: uuid.UUID,
    data_in: schema.ICartIn,
    user: User = Depends(UserWrite.current_user_with_data),
):
    return await service.update(data_in, user, cart_id)


@router.get("/")
async def get_carts(
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the Cart to be returned",
    ),
    per_page: int = 10,
    page: int = 1,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(default="id", description="order by attribute, e.g. id"),
    user: User = Depends(UserWrite.current_user_with_data),
):
    return await service.filter(
        user=user,
        select=select,
        per_page=per_page,
        page=page,
        sort_by=sort_by,
        order_by=order_by,
    )


@router.get("/{cart_id}", status_code=status.HTTP_200_OK)
async def get_cart(cart_id: uuid.UUID, user: User = Depends(UserWrite.current_user_with_data)):
    return await service.get(cart_id, user.id)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: uuid.UUID, user: User = Depends(UserWrite.current_user_with_data)):
    return await service.delete(cart_id, user)
