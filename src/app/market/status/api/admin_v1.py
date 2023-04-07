import uuid
from fastapi import APIRouter, Response, status
from src.app.market.status import schema, service


router = APIRouter(prefix="/status", tags=["Status"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(data_in: schema.IStatusIn) -> schema.IStatusOut:
    return await service.create(data_in=data_in)


@router.get(
    "/{status_id}",
    response_model=schema.IStatusOut,
    status_code=status.HTTP_200_OK,
)
async def get_category(status_id: uuid.UUID) -> schema.IStatusOut:
    return await service.get(status_id=status_id)


@router.put(
    "/{status_id}",
    response_model=schema.IStatusOut,
    status_code=status.HTTP_200_OK,
)
async def update_category(status_id: uuid.UUID, data_in: schema.IStatusIn):
    return await service.update(status_id=status_id, data_in=data_in)


@router.delete("/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(status_id: uuid.UUID) -> Response:
    return await service.delete(status_id=status_id)
