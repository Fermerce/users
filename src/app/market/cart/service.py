import typing as t
import uuid
from fastapi import status, Response
from src.app.user.model import User
from src.base.enum.sort_type import SortOrder
from src.lib.errors import error
from src.app.cart import schema, model
from src.app.cart.repository import cart_repo
from src.app.product.repository import product_property_repo, product_repo
from src.app.cart import validate


async def create(data_in: schema.ICartIn, user: User) -> model.Cart:
    product = await product_repo.get(id=data_in.product_id, load_related=True)
    await validate.validate_cart_data_on_create(data_in, product)
    new_cart = await cart_repo.create(obj=data_in, user=user, product=product)
    if not new_cart:
        raise error.BadDataError("Cannot add product to cart")
    await product_property_repo.update_quantity(
        paper_back_qty=data_in.paper_back_qty,
        hard_back_qty=data_in.hard_back_qty,
        property_id=product.property.id,
    )
    return new_cart


async def update(data_in: schema.ICartIn, user: User, cart_id: uuid.UUID) -> model.Cart:
    cart = await cart_repo.get_by_attr(
        attr=dict(user_id=user.id, id=cart_id, item_id=data_in.product_id),
        first=True,
        load_related=True,
    )
    if not cart:
        raise error.NotFoundError("Cart not found")
    await validate.validate_cart_data_on_update(data_in, cart.item.property)
    new_cart = await cart_repo.update(obj=data_in, cart_id=cart_id)
    if not new_cart:
        raise error.BadDataError("cannot update product quantity")
    await product_property_repo.update_quantity(
        paper_back_qty=data_in.paper_back_qty,
        hard_back_qty=data_in.hard_back_qty,
        property_id=cart.item.property.id,
    )

    return new_cart


async def get(cart_id: uuid.UUID, user_id: uuid.UUID) -> model.Cart:
    get_cart = await cart_repo.get_by_attr(
        attr=dict(id=cart_id, user_id=user_id), first=True, load_related=True
    )
    if not get_cart:
        raise error.NotFoundError("Cart not found")
    return get_cart


async def filter(
    user: User,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.Cart]:
    get_cart = await cart_repo.filter(
        per_page=per_page,
        page=page,
        select_columns=select,
        sort_by=sort_by,
        order_by=order_by,
        strict_search=dict(user_id=user.id),
        load_related=True,
    )
    return get_cart


async def delete(
    cart_id: uuid.UUID,
    user: User,
):
    get_cart = await cart_repo.get_by_attr(attr=dict(id=cart_id, user=user), first=True)
    if not get_cart:
        raise error.NotFoundError("Cart not found")
    await cart_repo.delete(cart_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
