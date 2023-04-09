import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.errors import error
from src.app.market.delivery_model import schema, model
from fastapi import Response
from src.app.market.delivery_model.repository import delivery_mode_repo


async def create(
    data_in: schema.IDeliveryModeIn,
) -> model.OrderDeliveryMode:
    check_delivery_mode = await delivery_mode_repo.get_by_attr(
        attr={"name": data_in.name}, first=True
    )
    if check_delivery_mode:
        raise error.DuplicateError("delivery mode already exists")
    new_delivery_mode = await delivery_mode_repo.create(obj=data_in)
    if not new_delivery_mode:
        raise error.ServerError("Internal server error")
    return new_delivery_mode


async def get(
    delivery_mode_id: uuid.UUID,
) -> model.OrderDeliveryMode:
    delivery_mode = await delivery_mode_repo.get(id=delivery_mode_id)
    if not delivery_mode:
        raise error.NotFoundError("delivery mode not found")
    return delivery_mode


async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.OrderDeliveryMode]:
    get_delivery_modes = await delivery_mode_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_delivery_modes


async def get_total_count() -> int:
    total = await delivery_mode_repo.get_count()
    return ITotalCount(count=total).dict()


async def update(
    delivery_mode_id: uuid.UUID,
    data_in: schema.IDeliveryModeIn,
) -> model.OrderDeliveryMode:
    check_mode = await delivery_mode_repo.get(id=delivery_mode_id)
    if not check_mode:
        raise error.NotFoundError("delivery mode does not exist")
    check_mode = await delivery_mode_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_mode and check_mode.id != delivery_mode_id:
        raise error.DuplicateError("delivery mode already exists")
    if await delivery_mode_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(
            f"delivery mode with name `{data_in.name}` already exists"
        )
    return await delivery_mode_repo.update(str(delivery_mode_id), data_in.dict())


async def delete(
    delivery_mode_id: uuid.UUID,
) -> None:
    check_mode = await delivery_mode_repo.get(id=delivery_mode_id)
    if not check_mode:
        raise error.NotFoundError("delivery mode does not exist")
    to_dele = await delivery_mode_repo.delete(delivery_mode_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
