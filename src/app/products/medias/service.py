import uuid
import typing as t
from fastapi import status
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount
from lib.exceptions.duplicate_error import DuplicateError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from src.app.products.medias import schema, model
from fastapi import Response
from src.app.products.medias.query import product_media_query


# create product category
async def create(
    data_in: schema.IProductMediaIn,
) -> model.ProductMedia:
    check_media = await product_media_query.get_by_attr(alt=data_in.alt)
    if check_media:
        raise DuplicateError("Media already exists")
    new_media = await product_media_query.create_obj(obj=data_in)
    if not new_media:
        raise ServerError("Internal server error")
    return new_media


# get product category
async def get(
    media_alt: uuid.UUID,
) -> model.ProductMedia:
    media = await product_media_query.get_by_attr(id=media_alt)
    if not media:
        raise NotFoundError("Media not found")
    return media


# get all media
async def filter(
    filter: str,
    page_size: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductMedia]:
    get_medias = await product_media_query.filter(
        filter_string=filter,
        page_size=page_size,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_medias


async def get_total_count() -> int:
    total = await product_media_query.get_count()
    return ITotalCount(count=total).dict()


# update product category
async def update(
    media_alt: uuid.UUID,
    data_in: schema.IProductMediaIn,
) -> model.ProductMedia:
    check_per = await product_media_query.get_by_attr(id=media_alt)
    if not check_per:
        raise NotFoundError("Media does not exist")
    check_per = await product_media_query.get_by_attr(alt=data_in.alt)
    if check_per and check_per.id != media_alt:
        raise DuplicateError("Media already exists")
    if await product_media_query.get_by_attr(alt=data_in.alt):
        raise DuplicateError(f"Media with name `{data_in.alt}` already exists")
    return await product_media_query.update(str(media_alt), data_in.dict())


# delete product category
async def delete(
    media_alt: uuid.UUID,
) -> None:
    check_per = await product_media_query.get_by_attr(id=media_alt)
    if not check_per:
        raise NotFoundError("Media does not exist")
    to_dele = await product_media_query.delete_obj(media_alt)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise ServerError("error deleting media")
