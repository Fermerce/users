import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.errors import error
from src.app.market.country import schema, model
from fastapi import Response
from src.app.market.country.repository import country_repo



# create permission
async def create(
    data_in: schema.ICountryIn,
) -> model.Country:
    check_type = await country_repo.get_by_attr(attr={"name": data_in.name}, first=True)
    if check_type:
        raise error.DuplicateError("country already exists")
    new_type = await country_repo.create(obj=data_in)
    if not new_type:
        raise error.ServerError("Internal server error")
    return new_type


# get permission
async def get(
    type_id: uuid.UUID,
) -> model.Country:
    perm = await country_repo.get(id=type_id)
    if not perm:
        raise error.NotFoundError("country not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.Country]:
    get_perms = await country_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> ITotalCount:
    total = await country_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    type_id: uuid.UUID,
    data_in: schema.ICountryIn,
) -> model.Country:
    check_type = await country_repo.get(id=type_id)
    if not check_type:
        raise error.NotFoundError("country does not exist")
    check_type = await country_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_type and check_type.id != type_id:
        raise error.DuplicateError("country already exists")
    if await country_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(f"country with name `{data_in.name}` already exists")
    return await country_repo.update(str(type_id), data_in.dict())


# delete permission
async def delete(
    type_id: uuid.UUID,
) -> None:
    check_type = await country_repo.get(id=type_id)
    if not check_type:
        raise error.NotFoundError("country does not exist")
    to_dele = await country_repo.delete(type_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

