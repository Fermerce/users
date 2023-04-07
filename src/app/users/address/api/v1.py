import typing as t
import uuid
from fastapi import APIRouter, Depends, Query, Response, status
from src.app.users.user.dependency import require_customer
from src.app.users.shipping_address import schema, service
from src.app.users.user.model import User

router = APIRouter(
    prefix="/shipping-addresses",
    tags=["Shipping shipping_address"],
    include_in_schema=True,
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=schema.IAddressOut
)
async def create_address(
    data_in: schema.IAddressIn,
    user: User = Depends(require_customer),
):
    return await service.create(data_in=data_in, user=user)


@router.get(
    "/",
    # response_model=t.List[schema.IAddressOut],
    status_code=status.HTTP_200_OK,
)
async def get_address_list(
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all through attributes"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="select specific attribute",
    ),
    user: User = Depends(require_customer),
    per_page: int = 10,
    page: int = 1,
):
    return await service.filter(
        filter=filter, per_page=per_page, page=page, user=user, select=select
    )


@router.get(
    "/{address_id}",
    response_model=schema.IAddressOut,
    status_code=status.HTTP_200_OK,
)
async def get_address(
    address_id: uuid.UUID,
    user: User = Depends(require_customer),
):
    return await service.get(address_id=address_id, user=user)


@router.put(
    "/{address_id}",
    status_code=status.HTTP_200_OK,
    response_model=schema.IAddressOut,
)
async def update_address(
    address_id: uuid.UUID,
    data_in: schema.IAddressIn,
    user: User = Depends(require_customer),
):
    return await service.update(address_id=address_id, data_in=data_in, user=user)


@router.get("/total/count", response_model=dict)
async def get_total_address(
    user: User = Depends(require_customer),
) -> t.Optional[int]:
    return await service.get_total_count(user)


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: uuid.UUID,
    user: User = Depends(require_customer),
) -> Response:
    return await service.delete(address_id, user)
