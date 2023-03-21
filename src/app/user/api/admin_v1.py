import typing as t
import uuid
from fastapi import APIRouter, Query, status
from src.app.permission.schema import IPermissionOut
from src.app.user import schema, service

# from src.apps.user.model import User
from src.lib.base.enum.sort_type import SortOrder
from src.lib.base.schema.response import ResponseMessage, ITotalCount

# from src.lib.shared.dependency import UserWrite

router = APIRouter(prefix="/users", tags=["Users"], include_in_schema=True)


@router.get("/")
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


@router.get("/total/count", response_model=ITotalCount)
async def get_total_users() -> ITotalCount:
    return await service.get_total_users()


@router.get("/{user_id}/roles", response_model=t.List[IPermissionOut])
async def get_user_roles(
    user_id: uuid.UUID,
):
    return await service.get_user_role(user_id)


@router.put("/{user_id}/roles", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: uuid.UUID,
    data_in: schema.IUserPermissionUpdate,
) -> ResponseMessage:
    return await service.add_user_role(user_id=user_id, data_in=data_in)


@router.delete("/{user_id}/roles", status_code=status.HTTP_200_OK)
async def remove_user_role(
    user_id: uuid.UUID,
    data_in: schema.IUserPermissionUpdate,
) -> ResponseMessage:
    return await service.remove_user_role(user_id=user_id, data_in=data_in)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: uuid.UUID, permanent: bool = False) -> None:
    return await service.remove_user_data(user_id=user_id, permanent=permanent)


@router.get(
    "/{user_id}", response_model=schema.IUserOut, status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: uuid.UUID,
) -> schema.IUserOut:
    return await service.get_user(user_id)


@router.get("/{user_id}/reviews", response_model=t.List[IPermissionOut])
async def get_user_reviews(
    user_id: uuid.UUID,
    per_page: int = 10,
    page: int = 1,
    sort_by: SortOrder = SortOrder.asc,
):
    return await service.get_user_review(
        user_id=user_id, per_page=per_page, page=page, sort_by=sort_by
    )
