import uuid
import typing as t
from fastapi import Response
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from src.app.products.promo_code import schema, model
from src.app.products.promo_code.query import product_promo_code_query


# create permission
async def create(
    data_in: schema.IProductPromoCodeIn,
) -> model.ProductPromoCode:
    check_perm = await product_promo_code_query.get_by_attr(code=data_in.code)
    if check_perm:
        raise DuplicateError("product promo code already exists")
    new_perm = await product_promo_code_query.create_obj(data_in=data_in)
    if not new_perm:
        raise ServerError("Internal server error")
    return new_perm


# get permission
async def get(
    promo_code_id: uuid.UUID,
) -> model.ProductPromoCode:
    perm = await product_promo_code_query.get_by_attr(id=promo_code_id)
    if not perm:
        raise NotFoundError("Product promo code not found")
    return perm


# get all permissions
async def filter(
    filter: str,
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductPromoCode]:
    get_perms = await product_promo_code_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_perms


async def get_total_count() -> ITotalCount:
    total = await product_promo_code_query.get_count()
    return ITotalCount(count=total).dict()


# update permission
async def update(
    promo_code_id: uuid.UUID,
    data_in: schema.IProductPromoCodeIn,
) -> model.ProductPromoCode:
    check_per = await product_promo_code_query.get_by_attr(id=promo_code_id)
    if not check_per:
        raise NotFoundError("Product promo code does not exist")
    check_per = await product_promo_code_query.get_by_attr(code=data_in.code)
    if check_per and check_per.id != promo_code_id:
        raise DuplicateError("Product promo code already exists")
    if await product_promo_code_query.get_by_attr(code=data_in.code):
        raise DuplicateError(
            f"Product promo code with code `{data_in.code}` already exists"
        )
    return await product_promo_code_query.update(str(promo_code_id), data_in.dict())


# delete permission
async def delete(
    promo_code_id: uuid.UUID,
) -> None:
    check_per = await product_promo_code_query.get_by_attr(id=promo_code_id)
    if not check_per:
        raise NotFoundError("Product promo code does not exist")
    to_dele = await product_promo_code_query.delete_obj(promo_code_id)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise ServerError("Error deleting product promo code")
