import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from src.app.users.user import schema, service
from src.app.users.staff import dependency
from core.enum.sort_type import SortOrder
from core.schema.response import ITotalCount


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=t.List[schema.IUserOutFull],
    response_model_exclude_unset=True,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_users_list(
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
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_total_users() -> ITotalCount:
    return await service.get_total_users()


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin)],
)
async def delete_user(data_in: schema.IUserRemove) -> None:
    return await service.remove_users_data(data_in=data_in)


@router.get(
    "/{users_id}",
    response_model=t.Union[schema.IUserOutFull, schema.IUserOut],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependency.require_super_admin_or_admin)],
)
async def get_user(
    users_id: uuid.UUID,
    load_related: bool = True,
) -> t.Union[schema.IUserOutFull, schema.IUserOut]:
    return await service.get_user(users_id, load_related)
