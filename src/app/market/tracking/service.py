import uuid
import typing as t
from fastapi import status, Response
from core.enum.sort_type import SortOrder
from core.schema.response import IResponseMessage
from lib.errors import error
from src.app.market.tracking import schema, model
from src.app.market.tracking.repository import tracking_repo

from src.app.market.order.repository import order_item_repo


async def create(data_in: schema.ITrackIn) -> model.Tracking:
    get_order_item = await order_item_repo.get_by_attr(
        attr=dict(tracking_id=data_in.item_tracking_id),
        first=True,
        load_related=True,
    )
    if not get_order_item:
        raise error.NotFoundError("order item not found")
    new_track = await tracking_repo.create(
        obj=dict(order_item_id=get_order_item.id, location=data_in.location)
    )
    if new_track:
        result = await order_item_repo.add_track(
            order_item=get_order_item, track=new_track
        )
        if result:
            return IResponseMessage(message="track created successfully")
    raise error.ServerError("Error while creating track")


async def update(track_id: uuid.UUID, data_in: schema.ITrackIn) -> model.Tracking:
    get_track = await tracking_repo.get(track_id)
    if not get_track:
        raise error.NotFoundError("track not found")
    check_track = await tracking_repo.get_by_attr(
        attr=dict(location=data_in.location), first=True
    )
    if get_track and check_track.id != get_track.id:
        raise error.DuplicateError(
            f"Track with location `{data_in.location}`already  exist"
        )
    return get_track


async def get(track_id: uuid.UUID) -> model.Tracking:
    get_track = await tracking_repo.get(track_id)
    if not get_track:
        raise error.BadDataError("Either product id or slug is required")
    return get_track


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
    sort_by: SortOrder = SortOrder.asc,
    order_by: str = None,
    load_related: bool = False,
) -> t.List[model.Tracking]:
    get_tracks = await tracking_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
        order_by=order_by,
        sort_by=sort_by,
        load_related=load_related,
    )
    return get_tracks


async def get_tracks_by_items(item_tracking_id: str) -> t.List[model.Tracking]:
    item_trackings = await tracking_repo.get_by_attr(
        attr=dict(tracking_id=item_tracking_id)
    )
    return item_trackings


async def delete(track_id: uuid.UUID) -> Response:
    get_track = await tracking_repo.get(track_id)
    if not get_track:
        raise error.NotFoundError("Track not found")
    await tracking_repo.delete(track_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
