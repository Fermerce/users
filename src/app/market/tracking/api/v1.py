import uuid
from fastapi import APIRouter, status
from src.app.product import service


router = APIRouter(prefix="/trackings", tags=["Tracking"])


@router.get("/{item_tracking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_order_item_trackings(item_tracking_id: uuid.UUID) -> None:
    return await service.get_tracks_by_items(item_tracking_id=item_tracking_id)
