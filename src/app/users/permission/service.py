import uuid
import typing as t
from fastapi import status
from src._base.enum.sort_type import SortOrder
from src.lib.db.config import Async_session
from src.lib.errors import error
from src._base.schema.response import ITotalCount
from src.app.users.permission import schema, model
from fastapi import Response
from src.app.users.permission.repository import permission_repo
from sqlalchemy import select


# create permission
async def create(
    data_in: schema.IPermissionIn,
) -> model.Permission:
    check_perm = await permission_repo.get_by_attr(
        attr={"name": data_in.name}, first=True
    )
    if check_perm:
        raise error.DuplicateError("Permission already exists")
    new_perm = await permission_repo.create(obj=data_in)
    if not new_perm:
        raise error.ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    permission_id: uuid.UUID,
) -> model.Permission:
    perm = await permission_repo.get(id=permission_id)
    if not perm:
        raise error.NotFoundError("Permission not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.Permission]:
    get_perms = await permission_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> int:
    total = await permission_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    permission_id: uuid.UUID,
    data_in: schema.IPermissionIn,
) -> model.Permission:
    check_per = await permission_repo.get(id=permission_id)
    if not check_per:
        raise error.NotFoundError("Permission does not exist")
    check_per = await permission_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_per and check_per.id != permission_id:
        raise error.DuplicateError("Permission already exists")
    if await permission_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(
            f"Permission with name `{data_in.name}` already exists"
        )
    return await permission_repo.update(str(permission_id), data_in.dict())


# delete permission
async def delete(
    permission_id: uuid.UUID,
) -> None:
    check_per = await permission_repo.get(id=permission_id)
    if not check_per:
        raise error.NotFoundError("Permission does not exist")
    to_dele = await permission_repo.delete(permission_id)
    print(to_dele)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.Permission)
        result = await session.execute(stm)
        return result.scalars().all()
