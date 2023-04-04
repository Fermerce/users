import typing as t
import uuid
from fastapi import APIRouter, Query, status

from src.app.product import service
from src.base.enum.sort_type import SortOrder

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=schema.IProductLongInfo,
)
async def get_product(product_id: uuid.UUID = None, slug: str = None):
    return await service.get(product_id=product_id, slug=slug)


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    # response_model=List[schema.IProductShortInfo],
)
async def get_all_products(
    filter: str = "",
    select: str = "",
    page: int = 1,
    per_page: int = 10,
    is_series: bool = False,
    is_active: bool = True,
    is_assigned: bool = False,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id, title", description="order by attribute, e.g. id"
    ),
    load_related: bool = False,
):
    return await service.filter(
        per_page=per_page,
        page=page,
        filter=filter,
        select=select,
        order_by=order_by,
        sort_by=sort_by,
        is_active=is_active,
        is_series=is_series,
        is_assigned=is_assigned,
        load_related=load_related,
    )
