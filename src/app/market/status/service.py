import typing as t
import uuid
from fastapi import status, Response
from core.enum.sort_type import SortOrder
from lib.errors import error
from src.app.market.status import schema, model
from src.app.market.status.repository import status_repo


async def create(data_in: schema.IStatusIn) -> model.Status:
    check_status = await status_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_status:
        raise error.DuplicateError("Status already exists")
    new_status = await status_repo.create(data_in)
    return new_status


async def get(
    status_id: uuid.UUID,
):
    get_status = await status_repo.get(status_id)
    if not get_status:
        raise error.NotFoundError("Status not found")
    return get_status


async def update(
    status_id: uuid.UUID,
    data_in: schema.IStatusIn,
):
    get_status = await status_repo.get(status_id)
    if not get_status:
        raise error.NotFoundError("Status not found")
    check_status = await status_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_status:
        raise error.DuplicateError("Status already exists")
    if get_status.name == data_in.name:
        raise error.DuplicateError("status already exists")
    result = await status_repo.update(id=status_id, obj=data_in)
    if result:
        return result
    raise error.ServerError("Error updating status")


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.Status]:
    get_statuses = await status_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        sort_by=sort_by,
        order_by=order_by,
    )
    return get_statuses


async def delete(
    status_id: str,
):
    get_status = await status_repo.get(status_id)
    if not get_status:
        raise error.NotFoundError("Status not found")
    await status_repo.delete(status_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
