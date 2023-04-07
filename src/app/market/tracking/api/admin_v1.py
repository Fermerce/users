import typing as t
import uuid
from fastapi import APIRouter, Query, status

from src.app.market.tracking import schema, service
from core.enum.sort_type import SortOrder


router = APIRouter(prefix="/trackings", tags=["Tracking"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tracking(data_in: schema.ITrackIn):
    return await service.create(data_in=data_in)


@router.get("/{track_id}", status_code=status.HTTP_201_CREATED)
async def create_tracking(track_id: uuid.UUID):
    return await service.get(track_id)


@router.put("/{track_id}", status_code=status.HTTP_201_CREATED)
async def update_tracking(track_id: uuid.UUID, data_in: schema.ITrackIn):
    return await service.update(track_id=track_id, data_in=data_in)


async def get_trackings(
    filter: str = "",
    select: str = "",
    page: int = 1,
    per_page: int = 10,
    sort_by: t.Optional[SortOrder] = Query(
        default=SortOrder.desc, description="order by attribute, e.g. id"
    ),
    order_by: t.Optional[str] = Query(
        default="id, title", description="order by attribute, e.g. id"
    ),
    load_related: bool = False,
):
    return await service.filter(
        per_page=per_page,
        page=page,
        filter=filter,
        select=select,
        order_by=order_by,
        sort_by=sort_by,
        load_related=load_related,
    )


@router.delete("/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tracking(track_id: uuid.UUID) -> None:
    return await service.delete(track_id=track_id)
