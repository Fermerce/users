import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.products.measuring_unit import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/measurements", tags=["Product measuring unit_id"])


@router.post(
    "/",
    # response_model=schema.IProductMeasuringUnitIn,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_measurement(
    data_in: schema.IProductMeasuringUnitIn,
) -> schema.IProductMeasuringUnitIn:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IProductMeasuringUnitIn],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_measurement_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the measurements",
    ),
    page_size: int = 10,
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
        page_size=page_size,
        page=page,
        select=select,
        order_by=order_by,
        sort_by=sort_by,
    )


@router.get(
    "/{unit_id}",
    # response_model=schema.IProductMeasuringUnitIn,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_measurement(unit_id: uuid.UUID) -> schema.IProductMeasuringUnitIn:
    return await service.get(unit_id=unit_id)


@router.put(
    "/{unit_id}",
    response_model=schema.IProductMeasuringUnitIn,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_measurement(
    unit_id: uuid.UUID, measurement: schema.IProductMeasuringUnitIn
) -> schema.IProductMeasuringUnitIn:
    return await service.update(unit_id=unit_id, data_in=measurement)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_measurement() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.get(
    "/example/testing",
    # response_model=int,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_measurement():
    return await service.example()


@router.delete(
    "/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_measurement(unit_id: uuid.UUID) -> None:
    return await service.delete(unit_id=unit_id)
