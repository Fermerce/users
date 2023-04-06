import uuid
import typing as t
from fastapi import status
from fastapi import Response
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from src.app.users.permission import schema, model

from src.app.users.permission.query import permission_query


# create permission
async def create(
    data_in: schema.IPermissionIn,
) -> model.Permission:
    check_perm = await permission_query.get_by_attr(first=True, name=data_in.name)
    if check_perm:
        raise DuplicateError("Permission already exists")
    new_perm = await permission_query.create_obj(data_in=data_in)
    if not new_perm:
        raise ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    permission_id: uuid.UUID,
) -> model.Permission:
    perm = await permission_query.get_by_attr(id=permission_id)
    if not perm:
        raise NotFoundError("Permission not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.Permission]:
    query = model.Permission.objects

    if filter:
        query = query.filter(name__icontains=filter)
    if order_by:
        if sort_by == SortOrder.asc:
            query = query.order_by(f"-{order_by}")
        query = query.order_by(f"{order_by}")

    objects = await query.all()
    # Count total number of objects
    total_count = len(objects)

    # Calculate offset and limit for pagination
    offset = (page - 1) * page_size
    limit = page_size

    # Apply offset and limit
    query = query.offset(offset).limit(limit)

    if select:
        objects = await query.values([val.strip() for val in select.split(",")])

    # Execute the query and retrieve the objects

    # Check if there are more pages
    has_next = (offset + limit) < total_count
    has_previous = offset > 0
    # Raise an exception if the requested page does not exist
    if page > 1 and not objects:
        raise NotFoundError("Page not found")

    return {
        "items": objects,
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "has_next": has_next,
        "has_previous": has_previous,
        "next_page": page + 1 if has_next else None,
        "previous_page": page - 1 if has_previous else None,
    }

    # print(get_perms)
    # return get_perms


async def get_total_count() -> int:
    total = await permission_query.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    permission_id: uuid.UUID,
    data_in: schema.IPermissionIn,
) -> model.Permission:
    check_per = await permission_query.get_by_attr(id=permission_id)
    if not check_per:
        raise NotFoundError("Permission does not exist")
    if check_per.name == data_in.name:
        raise DuplicateError(f"Permission with name `{data_in.name}` already exists")
    check_per = await permission_query.get_by_attr(name=data_in.name)
    if check_per and check_per.id != permission_id:
        raise DuplicateError("Permission already exists")
    if await permission_query.get_by_attr(name=data_in.name):
        raise DuplicateError(f"Permission with name `{data_in.name}` already exists")
    return await permission_query.update_obj(str(permission_id), data_in.dict())


# delete permission
async def delete(
    permission_id: uuid.UUID,
) -> None:
    model.Permission.objects.delete()
    check_per = await permission_query.get_by_attr(id=permission_id)
    if not check_per:
        raise NotFoundError("Permission does not exist")
    await permission_query.delete_obj(permission_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
