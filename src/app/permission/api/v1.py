import typing as t
import uuid

from fastapi import APIRouter, Query, status
from src.app.permission import schema, service

from src._base.enum.sort_type import SortOrder
from src._base.schema.response import IBaseResponse


router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post(
    "/",
    # response_model=IBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    data_in: schema.IPermissionIn,
) -> schema.IPermissionOut:
    return await service.create(data_in=data_in)


@router.get(
    "/",
)
# response_model=list[schema.IPermissionOut]
async def get_permission_list(
    # _: Customer = Depends(CustomerWrite.current_Customer_with_data),
    filter: t.Optional[str] = Query(default="", alias="filter", description="filter all address"),
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
    order_by: t.Optional[str] = Query(default="id", description="order by attribute, e.g. id"),
):
    return await service.filter(
        filter=filter,
        per_page=per_page,
        page=page,
        select=select,
        order_by=order_by,
        sort_by=sort_by,
    )


@router.get("/{permission_id}", response_model=schema.IPermissionOut)
async def get_permission(permission_id: uuid.UUID) -> schema.IPermissionOut:
    return await service.get(permission_id=permission_id)


@router.put("/{permission_id}", response_model=schema.IPermissionOut)
async def update_permission(
    permission_id: uuid.UUID, permission: schema.IPermissionIn
) -> schema.IPermissionOut:
    return await service.update(permission_id=permission_id, data_in=permission)


@router.get("/total/count", response_model=int)
async def get_total_permission() -> t.Optional[int]:
    return await service.get_total_count()


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(permission_id: uuid.UUID) -> None:
    return await service.delete(permission_id=permission_id)
