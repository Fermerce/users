import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.market.country import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/countries", tags=["Country"])


@router.post(
    "/",
    # response_model=schema.ICountryOut,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_country(
    data_in: schema.ICountryIn,
) -> schema.ICountryOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.ICountryOut],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_country_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all shipping_address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the countries",
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
    "/{country_id}",
    # response_model=schema.ICountryOut,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_country(country_id: uuid.UUID) -> schema.ICountryOut:
    return await service.get(country_id=country_id)


@router.put(
    "/{country_id}",
    response_model=schema.ICountryOut,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_country(
    country_id: uuid.UUID, type: schema.ICountryIn
) -> schema.ICountryOut:
    return await service.update(country_id=country_id, data_in=type)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_country() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.delete(
    "/{country_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_country(country_id: uuid.UUID) -> None:
    return await service.delete(country_id=country_id)
