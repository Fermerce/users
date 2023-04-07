import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.market.state import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/states", tags=["State"])


@router.post(
    "/",
    # response_model=schema.IStateOut,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_state(
    data_in: schema.IStateIn,
) -> schema.IStateOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IStateOut],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_state_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all shipping_address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the states",
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
    "/{state_id}",
    # response_model=schema.IStateOut,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_state(state_id: uuid.UUID) -> schema.IStateOut:
    return await service.get(state_id=state_id)


@router.put(
    "/{state_id}",
    response_model=schema.IStateOut,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_state(state_id: uuid.UUID, type: schema.IStateIn) -> schema.IStateOut:
    return await service.update(state_id=state_id, data_in=type)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_state() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.delete(
    "/{state_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_state(state_id: uuid.UUID) -> None:
    return await service.delete(state_id=state_id)
