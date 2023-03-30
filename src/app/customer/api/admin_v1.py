import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.customer import schema, service
from src.app.staff import dependency
from src._base.enum.sort_type import SortOrder
from src._base.schema.response import IResponseMessage, ITotalCount
from src.app.permission.schema import IPermissionOut


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get(
    "/",
    response_model=t.List[schema.ICustomerOutFull],
    response_model_exclude_unset=True
    # dependencies=[Depends(dependency.require_super_admin_or_admin)]
)
async def get_customers_list(
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
    load_related: t.Optional[bool] = False,
):
    return await service.filter(
        filter=filter,
        per_page=per_page,
        page=page,
        select=select,
        sort_by=sort_by,
        order_by=order_by,
        is_active=is_active,
        load_related=load_related,
    )


@router.get(
    "/total/count",
    response_model=ITotalCount,
    # dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_total_customers() -> ITotalCount:
    return await service.get_total_customers()


@router.get(
    "/{customer_id}/permissions",
    response_model=t.List[IPermissionOut],
    # dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_customer_permission(customer_id: uuid.UUID):
    return await service.get_customer_permissions(customer_id)


@router.put(
    "/permission",
    response_model=IResponseMessage,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def update_customer_permission(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    return await service.add_customer_permissions(data_in=data_in)


@router.delete(
    "/permission",
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def remove_customer_permission(
    data_in: schema.ICustomerRoleUpdate,
) -> IResponseMessage:
    return await service.remove_customer_permissions(data_in=data_in)


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(dependency.require_super_admin)],
)
async def delete_customer(data_in: schema.ICustomerRemove) -> None:
    return await service.remove_customer_data(data_in=data_in)


@router.get(
    "/{customer_id}",
    response_model=t.Union[schema.ICustomerOutFull, schema.ICustomerOut],
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_customer(
    customer_id: uuid.UUID,
    load_related: bool = True,
) -> t.Union[schema.ICustomerOutFull, schema.ICustomerOut]:
    return await service.get_customer(customer_id, load_related)
