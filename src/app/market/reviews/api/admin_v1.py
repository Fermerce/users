import typing as t
from fastapi import APIRouter, Depends, Response, status
from src.lib.shared.dependency import UserWrite
from src.app.reviews import service
from src.app.user.model import User


router = APIRouter(prefix="/reviews", tags=["Product Review"])


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str, _: User = Depends(UserWrite.is_super_admin)
) -> Response:
    return await service.delete(review_id=review_id)
