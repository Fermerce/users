import typing as t
import uuid
from fastapi import status, Response
from src.app.market.reviews.repository import review_repo
from src.app.market.status.repository import status_repo
from src.app.users.user.model import User
from core.enum.sort_type import SortOrder
from core.schema.response import IResponseMessage
from lib.errors import error
from src.app.market.order import schema, model
from src.app.market.order.repository import order_repo, order_item_repo
from src.app.market.cart.repository import cart_repo
from src.app.users.address.repository import address_repo


async def create(
    data_in: schema.IOrderIn,
    user: User,
) -> schema.IOrderSuccessOut:
    get_shipping_address = await address_repo.get_by_attr(
        attr=dict(id=data_in.address_id, user_id=user.id),
        first=True,
    )
    if not get_shipping_address:
        raise error.NotFoundError("Shipping shipping_address does not exist")
    get_carts = await cart_repo.get_cart_by_ids(user=user, cart_ids=data_in.cart_ids)
    if not get_carts:
        raise error.NotFoundError(
            "No product in cart, please add product to cart to continue"
        )

    new_order = await order_repo.create(
        obj=dict(
            user_id=user.id,
            shipping_address_id=get_shipping_address.id,
        )
    )
    order_status = await status_repo.get_by_attr(attr=dict(name="pending"), first=True)
    if not order_status:
        order_status = await status_repo.create(obj=dict(name="pending"))
    order_item_list: t.List[dict] = [
        dict(
            pdf=item.pdf,
            paper_back_qty=item.paper_back_qty,
            hard_back_qty=item.hard_back_qty,
            product_id=item.item_id,
            order_id=new_order.id,
            status_id=order_status.id,
        )
        for item in get_carts
        if new_order
    ]

    if new_order and len(order_item_list) > 0:
        new_order_items = await order_item_repo.create_many(objs=order_item_list)
        if new_order_items:
            await cart_repo.delete_many(ids=[cart.id for cart in get_carts])
            return schema.IOrderSuccessOut(order_id=new_order.order_id)
        raise error.ServerError("Error creating order, please try again")
    raise error.ServerError("Error creating order, please try again")


async def update_order_status(data_in: schema.IOrderUpdate) -> dict:
    get_user_order = await order_repo.get(data_in.order_id)
    if get_user_order is None:
        raise error.NotFoundError("Order is not found")
    get_status = await status_repo.get(data_in.status_id)
    if not get_status:
        raise error.NotFoundError("Status is not found")
    result = await order_repo.update(
        id=get_user_order.id, obj=dict(status_id=get_status.id)
    )
    if result:
        return IResponseMessage(message="Order status updated successfully")
    raise error.ServerError("Error updating order status, please try again")


async def update_order_item_status(
    data_in: schema.IOrderItemUpdate,
) -> IResponseMessage:
    get_user_order_item = await order_item_repo.get_by_attr(
        attr=dict(tracking_id=data_in.item_tracking_id),
        first=True,
        load_related=True,
    )
    if get_user_order_item is None:
        raise error.NotFoundError("product is not found in your order")
    if data_in.delivered == True:
        create_review = await review_repo.create(
            obj=dict(
                product_id=get_user_order_item.product.id,
                user_id=get_user_order_item.order.user_id,
            )
        )
        if create_review:
            return IResponseMessage(message="Item delivered successfully")
        raise error.ServerError("Error moving product to review")
    else:
        result = await order_repo.update(
            id=get_user_order_item.id, obj=dict(delivered=data_in.delivered)
        )
        if result:
            return IResponseMessage(message="order item updated successfully")
        return IResponseMessage(message="Item delivered successfully")


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    order_by: str = "",
    sort_by: t.Optional[SortOrder] = SortOrder.asc,
    load_related: bool = False,
) -> model.Order:
    order = await order_repo.filter(
        filter_string=filter,
        select_columns=select,
        per_page=per_page,
        page=page,
        sort_by=sort_by,
        order_by=order_by,
        load_related=load_related,
    )
    if order:
        return order
    raise error.NotFoundError("order not found")


async def get_orders(
    user: User,
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    order_by: str = "",
    sort_by: t.Optional[SortOrder] = SortOrder.asc,
    load_related: bool = False,
) -> model.Order:
    order = await order_repo.filter(
        filter_string=filter,
        select_columns=select,
        per_page=per_page,
        page=page,
        sort_by=sort_by,
        order_by=order_by,
        strict_search=dict(user=user),
        load_related=load_related,
    )
    if order:
        return order
    raise error.NotFoundError("order not found")


async def get_order(
    user: User,
    order_id: str,
) -> model.Order:
    order = await order_repo.get_by_attr(
        attr=dict(order_id=order_id, user=user), load_related=True, first=True
    )
    if order:
        return order
    raise error.NotFoundError("order not found")


async def get_order_items(
    user: User,
    order_id: str,
) -> model.Order:
    order = await order_repo.get_by_attr(
        attr=dict(order_id=order_id, user=user), first=True, load_related=True
    )
    if order:
        return order.items
    raise error.NotFoundError("order not found")


async def delete_order(order_id: str) -> None:
    check_order = await order_repo.get_by_attr(attr=dict(order_id=order_id), first=True)
    if not check_order:
        raise error.NotFoundError("Order item not found in your order")
    if not check_order.status.name != "completed":
        raise error.BadDataError("Order in progress can not be deleted")
    if await order_repo.delete(id=check_order.id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise error.ServerError("Error deleting order item, please try again")
