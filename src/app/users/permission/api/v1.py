import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.users.permission import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post(
    "/",
    response_model=schema.IPermissionOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_permission(
    data_in: schema.IPermissionIn,
) -> schema.IPermissionOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IPermissionOut],
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_permission_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all shipping_address"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the permissions",
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
    "/{permission_id}",
    response_model=schema.IPermissionOut,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_permission(permission_id: uuid.UUID) -> schema.IPermissionOut:
    return await service.get(permission_id=permission_id)


@router.put(
    "/{permission_id}",
    response_model=schema.IPermissionOut,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_permission(
    permission_id: uuid.UUID, permission: schema.IPermissionIn
) -> schema.IPermissionOut:
    return await service.update(permission_id=permission_id, data_in=permission)


@router.get(
    "/total/count",
    response_model=int,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_total_permission() -> t.Optional[int]:
    return await service.get_total_count()


@router.delete(
    "/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_permission(permission_id: uuid.UUID) -> None:
    return await service.delete(permission_id=permission_id)
