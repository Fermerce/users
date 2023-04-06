import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.db.config import Async_session
from lib.errors import error
from src.app.product.category import schema, model
from fastapi import Response
from src.app.product.category.repository import product_category_repo
from sqlalchemy import select


# create product category
async def create(
    data_in: schema.IProductCategoryIn,
) -> model.ProductCategory:
    check_perm = await product_category_repo.get_by_attr(
        attr={"name": data_in.name}, first=True
    )
    if check_perm:
        raise error.DuplicateError("Product category already exists")
    new_perm = await product_category_repo.create(obj=data_in)
    if not new_perm:
        raise error.ServerError("Internal server error")
    return new_perm


# get product category
async def get(
    product_category_id: uuid.UUID,
) -> model.ProductCategory:
    perm = await product_category_repo.get(id=product_category_id)
    if not perm:
        raise error.NotFoundError("Product category not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductCategory]:
    get_perms = await product_category_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> int:
    total = await product_category_repo.get_count()
    return ITotalCount(count=total).dict()


# update product category
async def update(
    product_category_id: uuid.UUID,
    data_in: schema.IProductCategoryIn,
) -> model.ProductCategory:
    check_per = await product_category_repo.get(id=product_category_id)
    if not check_per:
        raise error.NotFoundError("Product category does not exist")
    check_per = await product_category_repo.get_by_attr(
        attr=dict(name=data_in.name), first=True
    )
    if check_per and check_per.id != product_category_id:
        raise error.DuplicateError("Product category already exists")
    if await product_category_repo.get_by_attr(attr={"name": data_in.name}):
        raise error.DuplicateError(
            f"Product category with name `{data_in.name}` already exists"
        )
    return await product_category_repo.update(str(product_category_id), data_in.dict())


# delete product category
async def delete(
    product_category_id: uuid.UUID,
) -> None:
    check_per = await product_category_repo.get(id=product_category_id)
    if not check_per:
        raise error.NotFoundError("Product category does not exist")
    to_dele = await product_category_repo.delete(product_category_id)
    print(to_dele)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.ProductCategory)
        result = await session.execute(stm)
        return result.scalars().all()
