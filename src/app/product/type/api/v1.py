import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src._base.schema.response import ITotalCount
from src.app.product.type import schema, service
from src._base.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/types", tags=["Product Types"])


@router.post(
    "/",
    # response_model=schema.IProductTypeOut,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_type(
    data_in: schema.IProductTypeIn,
) -> schema.IProductTypeOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IProductTypeOut],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_type_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the types",
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
    "/{type_id}",
    # response_model=schema.IProductTypeOut,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_type(type_id: uuid.UUID) -> schema.IProductTypeOut:
    return await service.get(type_id=type_id)


@router.put(
    "/{type_id}",
    response_model=schema.IProductTypeOut,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_type(
    type_id: uuid.UUID, type: schema.IProductTypeIn
) -> schema.IProductTypeOut:
    return await service.update(type_id=type_id, data_in=type)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_type() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.get(
    "/example/testing",
    # response_model=int,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_type():
    return await service.example()


@router.delete(
    "/{type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_type(type_id: uuid.UUID) -> None:
    return await service.delete(type_id=type_id)
