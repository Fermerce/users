import uuid
import typing as t
from fastapi import Depends, status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.db.config import Async_session
from lib.errors import error
from src.app.product.promo_code import schema, model
from fastapi import Response
from src.app.product.promo_code.repository import product_promo_code_repo
from sqlalchemy import select


# create permission
async def create(
    data_in: schema.IProductPromoCodeIn,
) -> model.ProductPromoCode:
    check_perm = await product_promo_code_repo.get_by_attr(
        attr={"code": data_in.code}, first=True
    )
    if check_perm:
        raise error.DuplicateError("product promo code already exists")
    new_perm = await product_promo_code_repo.create(obj=data_in)

    if not new_perm:
        raise error.ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    promo_code_id: uuid.UUID,
) -> model.ProductPromoCode:
    perm = await product_promo_code_repo.get(id=promo_code_id)
    if not perm:
        raise error.NotFoundError("Product promo code not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductPromoCode]:
    get_perms = await product_promo_code_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> ITotalCount:
    total = await product_promo_code_repo.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    promo_code_id: uuid.UUID,
    data_in: schema.IProductPromoCodeIn,
) -> model.ProductPromoCode:
    check_per = await product_promo_code_repo.get(id=promo_code_id)
    if not check_per:
        raise error.NotFoundError("Product promo code does not exist")
    check_per = await product_promo_code_repo.get_by_attr(
        attr=dict(code=data_in.code), first=True
    )
    if check_per and check_per.id != promo_code_id:
        raise error.DuplicateError("Product promo code already exists")
    if await product_promo_code_repo.get_by_attr(attr={"code": data_in.code}):
        raise error.DuplicateError(
            f"Product promo code with code `{data_in.code}` already exists"
        )
    return await product_promo_code_repo.update(str(promo_code_id), data_in.dict())


# delete permission
async def delete(
    promo_code_id: uuid.UUID,
) -> None:
    check_per = await product_promo_code_repo.get(id=promo_code_id)
    if not check_per:
        raise error.NotFoundError("Product promo code does not exist")
    to_dele = await product_promo_code_repo.delete(promo_code_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.ProductPromoCode)
        result = await session.execute(stm)
        return result.scalars().all()
