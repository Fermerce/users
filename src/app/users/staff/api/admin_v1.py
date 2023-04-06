import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.users.permission.schema import IPermissionOut
from src.app.users.staff import schema, service, dependency
from core.enum.sort_type import SortOrder
from core.schema.response import IResponseMessage, ITotalCount


router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=IResponseMessage,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def create_staff(data_in: schema.IStaffIn) -> IResponseMessage:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_staff_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter through all attributes"
    ),
    select: t.Optional[str] = Query(
        default="", alias="select", description="select specific attributes"
    ),
    per_page: int = 10,
    page: int = 1,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id", description="order by attribute, e.g. id"
    ),
    is_active: t.Optional[bool] = True,
):
    return await service.filter(
        filter=filter,
        per_page=per_page,
        page=page,
        select=select,
        sort_by=sort_by,
        order_by=order_by,
        is_active=is_active,
    )


@router.get(
    "/total/count",
    response_model=ITotalCount,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_total_staff() -> ITotalCount:
    return await service.get_total_Staffs()


@router.get(
    "/{staff_id}/permissions",
    response_model=t.List[IPermissionOut],
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_staff_permissions(
    staff_id: uuid.UUID,
):
    return await service.get_staff_permissions(staff_id)


@router.put(
    "/permissions",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def update_staff_permissions(
    data_in: schema.IStaffRoleUpdate,
) -> IResponseMessage:
    return await service.add_staff_permission(data_in=data_in)


@router.delete(
    "/permissions",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin)],
)
async def remove_staff_permissions(
    data_in: schema.IStaffRoleUpdate,
) -> IResponseMessage:
    return await service.remove_staff_permissions(data_in=data_in)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin)],
)
async def delete_staff(data_in: schema.IRemoveStaff) -> None:
    return await service.remove_staff_data(data_in)


@router.get(
    "/{staff_id}",
    response_model=t.Union[schema.IStaffOutFull, schema.IStaffOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_staff(
    staff_id: uuid.UUID,
    load_related: bool = False,
) -> t.Union[schema.IStaffOutFull, schema.IStaffOut]:
    return await service.get_staff(staff_id, load_related)
