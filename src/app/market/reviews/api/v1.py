import typing as t
from fastapi import APIRouter, Depends, status, Query
from src.lib.shared.dependency import UserWrite
from src.app.reviews import schema, service
from src.app.user.model import User


router = APIRouter(prefix="/reviews", tags=["Product Review"], include_in_schema=True)


@router.get("/", response_model=t.List[schema.IReviewOut])
async def get_review_list(
    _: User = Depends(UserWrite.super_or_admin),
    filter: t.Optional[str] = Query(
        default="", alias="filter", description="filter all reviews"
    ),
    select: t.Optional[str] = Query(
        default="",
        alias="select",
        description="specific attributes of the shipping_address",
    ),
    per_page: int = 10,
    page: int = 1,
) -> t.List[schema.IReviewOut]:
    return await service.filter(
        filter=filter, per_page=per_page, page=page, select=select
    )


@router.get("/total", response_model=int)
async def get_total_reviews() -> t.Optional[int]:
    return await service.get_total_count()


@router.put(
    "/{review_id}",
    response_model=schema.IReviewOut,
    status_code=status.HTTP_200_OK,
)
async def update_review(
    review_id: str,
    data_in: schema.IReviewIn,
    user: User = Depends(UserWrite.current_user_with_data),
):
    return await service.update(review_id=review_id, data_in=data_in, user=user)
