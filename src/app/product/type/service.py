import uuid
import typing as t
from fastapi import status
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import ITotalCount
from src.lib.db.config import Async_session
from src.lib.errors import error
from src.app.product.type import schema, model
from fastapi import Response
from src.app.product.type.repository import product_type_repo
from sqlalchemy import select


# create permission
async def create(
    data_in: schema.IProductTypeIn,
) -> model.ProductType:
    check_type = await product_type_repo.get_by_attr(
        attr={"name": data_in.name}, first=True
    )
    if check_type:
        raise error.DuplicateError("product type already exists")
    new_type = await product_type_repo.create(obj=data_in)
    if not new_type:
        raise error.ServerError("Internal server error")
    return new_type


# get permission
async def get(
    type_id: uuid.UUID,
) -> model.ProductType:
    perm = await product_type_repo.get(id=type_id)
    if not perm:
        raise error.NotFoundError("product type not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductType]:
    get_perms = await product_type_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> ITotalCount:
    total = await product_type_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    type_id: uuid.UUID,
    data_in: schema.IProductTypeIn,
) -> model.ProductType:
    check_type = await product_type_repo.get(id=type_id)
    if not check_type:
        raise error.NotFoundError("product type does not exist")
    check_type = await product_type_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_type and check_type.id != type_id:
        raise error.DuplicateError("product type already exists")
    if await product_type_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(
            f"product type with name `{data_in.name}` already exists"
        )
    return await product_type_repo.update(str(type_id), data_in.dict())


# delete permission
async def delete(
    type_id: uuid.UUID,
) -> None:
    check_type = await product_type_repo.get(id=type_id)
    if not check_type:
        raise error.NotFoundError("product type does not exist")
    to_dele = await product_type_repo.delete(type_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.ProductType)
        result = await session.execute(stm)
        return result.scalars().all()
