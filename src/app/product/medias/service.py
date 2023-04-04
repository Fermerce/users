import uuid
import typing as t
from fastapi import status
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import ITotalCount
from src.lib.db.config import Async_session
from src.lib.errors import error
from src.app.product.medias import schema, model
from fastapi import Response
from src.app.product.medias.repository import product_media_repo
from sqlalchemy import select


# create product category
async def create(
    data_in: schema.IProductMediaIn,
) -> model.ProductMedia:
    check_media = await product_media_repo.get_by_attr(
        attr={"alt": data_in.alt}, first=True
    )
    if check_media:
        raise error.DuplicateError("Media already exists")
    new_media = await product_media_repo.create(obj=data_in)
    if not new_media:
        raise error.ServerError("Internal server error")
    return new_media


# get product category
async def get(
    media_alt: uuid.UUID,
) -> model.ProductMedia:
    media = await product_media_repo.get(id=media_alt)
    if not media:
        raise error.NotFoundError("Media not found")
    return media


# get all media
async def filter(
    filter: str,
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
) -> t.List[model.ProductMedia]:
    get_medias = await product_media_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
    )
    return get_medias


async def get_total_count() -> int:
    total = await product_media_repo.get_count()
    return ITotalCount(count=total).dict()


# update product category
async def update(
    media_alt: uuid.UUID,
    data_in: schema.IProductMediaIn,
) -> model.ProductMedia:
    check_per = await product_media_repo.get(id=media_alt)
    if not check_per:
        raise error.NotFoundError("Media does not exist")
    check_per = await product_media_repo.get_by_attr(
        attr=dict(name=data_in.alt), first=True
    )
    if check_per and check_per.id != media_alt:
        raise error.DuplicateError("Media already exists")
    if await product_media_repo.get_by_attr(attr={"name": data_in.alt}):
        raise error.DuplicateError(f"Media with name `{data_in.alt}` already exists")
    return await product_media_repo.update(str(media_alt), data_in.dict())


# delete product category
async def delete(
    media_alt: uuid.UUID,
) -> None:
    check_per = await product_media_repo.get(id=media_alt)
    if not check_per:
        raise error.NotFoundError("Media does not exist")
    to_dele = await product_media_repo.delete(media_alt)
    if to_dele:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


async def example():
    async with Async_session() as session:
        stm = select(model.ProductMedia)
        result = await session.execute(stm)
        return result.scalars().all()
