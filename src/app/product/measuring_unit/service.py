import uuid
import typing as t
from fastapi import Depends, status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.db.config import Async_session
from lib.errors import error
from src.app.product.measuring_unit import schema, model
from fastapi import Response
from src.app.product.measuring_unit.repository import product_measuring_unit_repo
from sqlalchemy import select


# create permission
async def create(
    data_in: schema.IProductMeasuringUnitIn,
) -> model.ProductMeasuringUnit:
    check_unit = await product_measuring_unit_repo.get_by_attr(
        attr={"unit": data_in.unit}, first=True
    )
    if check_unit:
        raise error.DuplicateError(" product measuring unit already exists")
    new_perm = await product_measuring_unit_repo.create(obj=data_in)
    if not new_perm:
        raise error.ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    unit_id: uuid.UUID,
) -> model.ProductMeasuringUnit:
    perm = await product_measuring_unit_repo.get(id=unit_id)
    if not perm:
        raise error.NotFoundError(" product measuring unit not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductMeasuringUnit]:
    get_perms = await product_measuring_unit_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> int:
    total = await product_measuring_unit_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    unit_id: uuid.UUID,
    data_in: schema.IProductMeasuringUnitIn,
) -> model.ProductMeasuringUnit:
    check_per = await product_measuring_unit_repo.get(id=unit_id)
    if not check_per:
        raise error.NotFoundError(" product measuring unit does not exist")
    check_per = await product_measuring_unit_repo.get_by_attr(
        attr=dict(unit=data_in.unit), first=True
    )
    if check_per and check_per.id != unit_id:
        raise error.DuplicateError(" product measuring unit already exists")
    if await product_measuring_unit_repo.get_by_attr(attr={"unit": data_in.unit}):
        raise error.DuplicateError(
            f" product measuring unit with unit `{data_in.unit}` already exists"
        )
    return await product_measuring_unit_repo.update(str(unit_id), data_in.dict())


# delete permission
async def delete(
    unit_id: uuid.UUID,
) -> None:
    check_per = await product_measuring_unit_repo.get(id=unit_id)
    if not check_per:
        raise error.NotFoundError(" product measuring unit does not exist")
    to_dele = await product_measuring_unit_repo.delete(unit_id)
    print(to_dele)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.ProductMeasuringUnit)
        result = await session.execute(stm)
        return result.scalars().all()
