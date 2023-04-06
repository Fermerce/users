import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from src.app.products.category import schema, model
from fastapi import Response
from src.app.products.category.query import product_category_query


# create product category
async def create(
    data_in: schema.IProductCategoryIn,
) -> model.ProductCategory:
    check_perm = await product_category_query.get_by_attr(name=data_in.name)
    if check_perm:
        raise DuplicateError("Product category already exists")
    new_perm = await product_category_query.create_obj(obj=data_in)
    if not new_perm:
        raise ServerError("Internal server error")
    return new_perm


# get product category
async def get(
    product_category_id: uuid.UUID,
) -> model.ProductCategory:
    perm = await product_category_query.get_by_attr(id=product_category_id)
    if not perm:
        raise NotFoundError("Product category not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductCategory]:
    get_perms = await product_category_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> int:
    total = await product_category_query.get_count()
    return ITotalCount(count=total).dict()


# update product category
async def update(
    product_category_id: uuid.UUID,
    data_in: schema.IProductCategoryIn,
) -> model.ProductCategory:
    check_per = await product_category_query.get_by_attr(id=product_category_id)
    if not check_per:
        raise NotFoundError("Product category does not exist")
    check_per = await product_category_query.get_by_attr(name=data_in.name)
    if check_per and check_per.id != product_category_id:
        raise DuplicateError("Product category already exists")
    if await product_category_query.get_by_attr(name=data_in.name):
        raise DuplicateError(
            f"Product category with name `{data_in.name}` already exists"
        )
    return await product_category_query.update_obj(
        str(product_category_id), data_in.dict()
    )


# delete product category
async def delete(
    product_category_id: uuid.UUID,
) -> None:
    check_per = await product_category_query.get(id=product_category_id)
    if not check_per:
        raise NotFoundError("Product category does not exist")
    to_dele = await product_category_query.delete_obj(product_category_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise ServerError("Error deleting product category")
