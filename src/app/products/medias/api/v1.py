import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.products.medias import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/statics", tags=["Product statics files"])


@router.post(
    "/",
    # response_model=schema.IProductMediaIn,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_permission(
    data_in: schema.IProductMediaIn,
) -> schema.IProductMediaIn:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IProductMediaIn],
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_permission_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the categories",
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
    "/{media_alt}",
    # response_model=schema.IProductMediaIn,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_permission(media_alt: uuid.UUID) -> schema.IProductMediaIn:
    return await service.get(media_alt=media_alt)


@router.put(
    "/{media_alt}",
    response_model=schema.IProductMediaIn,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_permission(
    media_alt: uuid.UUID, permission: schema.IProductMediaIn
) -> schema.IProductMediaIn:
    return await service.update(media_alt=media_alt, data_in=permission)


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_permission() -> t.Optional[ITotalCount]:
    return await service.get_total_count()


@router.get(
    "/example/testing",
    # response_model=int,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_permission():
    return await service.example()


@router.delete(
    "/{media_alt}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_permission(media_alt: uuid.UUID) -> None:
    return await service.delete(media_alt=media_alt)
