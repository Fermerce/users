import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.product.promo_code import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/promocodes", tags=["ProductPromoCodes"])


@router.post(
    "/",
    # response_model=schema.IProductPromoCodeOut,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_promo_code(
    data_in: schema.IProductPromoCodeIn,
) -> schema.IProductPromoCodeOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IProductPromoCodeOut],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_promo_code_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all shipping_address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the promo_codes",
    ),
    per_page: int = 10,
    page: int = 1,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id", description="order by attribute, e.g. id"
    ),
):
    return await service.filter(
        filter=filter,
        per_page=per_page,
        page=page,
        select=select,
        order_by=order_by,
        sort_by=sort_by,
    )


@router.get(
    "/{promo_code_id}",
    # response_model=schema.IProductPromoCodeOut,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_promo_code(promo_code_id: uuid.UUID) -> schema.IProductPromoCodeOut:
    return await service.get(promo_code_id=promo_code_id)


@router.put(
    "/{promo_code_id}",
    response_model=schema.IProductPromoCodeOut,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_promo_code(
    promo_code_id: uuid.UUID, data_in: schema.IProductPromoCodeIn
) -> schema.IProductPromoCodeOut:
    return await service.update(promo_code_id=promo_code_id, data_in=data_in)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_promo_code() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.get(
    "/example/testing",
    # response_model=int,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_promo_code():
    return await service.example()


@router.delete(
    "/{promo_code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_promo_code(promo_code_id: uuid.UUID) -> None:
    return await service.delete(promo_code_id=promo_code_id)
