import uuid
import typing as t
from fastapi import Depends, status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from src.app.products.measuring_unit import schema, model
from fastapi import Response
from src.app.products.measuring_unit.query import product_measuring_unit_query



# create permission
async def create(
    data_in: schema.IProductMeasuringUnitIn,
) -> model.ProductMeasuringUnit:
    check_unit = await product_measuring_unit_query.get_by_attr(
        attr={"unit": data_in.unit}, first=True
    )
    if check_unit:
        raise DuplicateError(" product measuring unit already exists")
    new_perm = await product_measuring_unit_query.create_obj(obj=data_in)
    if not new_perm:
        raise ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    unit_id: uuid.UUID,
) -> model.ProductMeasuringUnit:
    perm = await product_measuring_unit_query.get_by_attr(id=unit_id)
    if not perm:
        raise NotFoundError(" product measuring unit not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductMeasuringUnit]:
    get_perms = await product_measuring_unit_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> int:
    total = await product_measuring_unit_query.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    unit_id: uuid.UUID,
    data_in: schema.IProductMeasuringUnitIn,
) -> model.ProductMeasuringUnit:
    check_per = await product_measuring_unit_query.get_by_attr(id=unit_id)
    if not check_per:
        raise NotFoundError(" product measuring unit does not exist")
    check_per = await product_measuring_unit_query.get_by_attr(unit=data_in.unit)
    if check_per and check_per.id != unit_id:
        raise DuplicateError(" product measuring unit already exists")
    if await product_measuring_unit_query.get_by_attr(unit=data_in.unit):
        raise DuplicateError(
            f" product measuring unit with unit `{data_in.unit}` already exists"
        )
    return await product_measuring_unit_query.update_obj(str(unit_id), data_in.dict())


# delete permission
async def delete(
    unit_id: uuid.UUID,
) -> None:
    check_per = await product_measuring_unit_query.get_by_attr(id=unit_id)
    if not check_per:
        raise NotFoundError(" product measuring unit does not exist")
    to_dele = await product_measuring_unit_query.delete_obj(unit_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise ServerError("Error deleting product measurement unit")
