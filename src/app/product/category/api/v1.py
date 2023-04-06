import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, status
from core.schema.response import ITotalCount
from src.app.product.category import schema, service
from core.enum.sort_type import SortOrder
from src.app.users.staff.dependency import require_super_admin_or_admin


router = APIRouter(prefix="/categories", tags=["Product Category"])


@router.post(
    "/",
    # response_model=schema.IProductCategoryIn,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def create_permission(
    data_in: schema.IProductCategoryIn,
) -> schema.IProductCategoryIn:
    return await service.create(data_in=data_in)


@router.get(
    "/",
    response_model=list[schema.IProductCategoryIn],
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
    "/{product_category_id}",
    # response_model=schema.IProductCategoryIn,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def get_permission(product_category_id: uuid.UUID) -> schema.IProductCategoryIn:
    return await service.get(product_category_id=product_category_id)


@router.put(
    "/{product_category_id}",
    response_model=schema.IProductCategoryIn,
    dependencies=[Depends(require_super_admin_or_admin)],
)
async def update_permission(
    product_category_id: uuid.UUID, permission: schema.IProductCategoryIn
) -> schema.IProductCategoryIn:
    return await service.update(
        product_category_id=product_category_id, data_in=permission
    )


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
    "/{product_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(require_super_admin_or_admin)],
)
async def delete_permission(product_category_id: uuid.UUID) -> None:
    return await service.delete(product_category_id=product_category_id)
