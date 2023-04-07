import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.errors import error
from src.app.market.state import schema, model
from fastapi import Response
from src.app.market.state.repository import state_repo



# create permission
async def create(
    data_in: schema.IStateIn,
) -> model.State:
    check_state = await state_repo.get_by_attr(attr={"name": data_in.name}, first=True)
    if check_state:
        raise error.DuplicateError("state already exists")
    new_state = await state_repo.create(obj=data_in)
    if not new_state:
        raise error.ServerError("Internal server error")
    return new_state


# get permission
async def get(
    state_id: uuid.UUID,
) -> model.State:
    perm = await state_repo.get(id=state_id)
    if not perm:
        raise error.NotFoundError("state not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.State]:
    get_perms = await state_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> ITotalCount:
    total = await state_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    state_id: uuid.UUID,
    data_in: schema.IStateIn,
) -> model.State:
    check_state = await state_repo.get(id=state_id)
    if not check_state:
        raise error.NotFoundError("state does not exist")
    check_state = await state_repo.get_by_attr(attr=dict(name=data_in.name), first=True)
    if check_state and check_state.id != state_id:
        raise error.DuplicateError("state already exists")
    if await state_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(f"state with name `{data_in.name}` already exists")
    return await state_repo.update(str(state_id), data_in.dict())


# delete permission
async def delete(
    state_id: uuid.UUID,
) -> None:
    check_state = await state_repo.get(id=state_id)
    if not check_state:
        raise error.NotFoundError("state does not exist")
    to_dele = await state_repo.delete(state_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
