import typing as t
from fastapi import status, Response
from src.app.user.model import User
from src.lib.errors import error
from src.app.reviews import schema, model
from src.app.reviews.repository import review_repo


async def update(
    review_id: str,
    data_in: schema.IReviewIn,
    user: User,
) -> model.Review:
    check_review = await review_repo.get_by_attr(attr=dict(id=review_id, user=user))
    if not check_review:
        raise error.NotFoundError("Product does not exist")
    if check_review.edit_limit == 3:
        raise error.ForbiddenError("You have reached the edit limit")
    updated_review = await review_repo.update(
        id=check_review.id,
        obj=dict(
            **data_in.dict(
                exclude={"product_id"},
                reviewed=True,
                user=user,
                edit_limit=check_review.edit_limit + 1,
            )
        ),
    )
    if updated_review:
        return updated_review
    raise error.ServerError("error updating review")


async def filter(
    filter: str = "",
    per_page: int = 10,
    page: int = 0,
    select: str = "",
) -> t.List[model.Review]:
    get_reviews = await review_repo.filter(
        filter_string=filter,
        per_page=per_page,
        page=page,
        select_columns=select,
    )
    return get_reviews


async def get_total_count() -> int:
    return await review_repo.get_count()


async def delete(
    review_id: str,
) -> None:
    get_review = await review_repo.get(id=review_id)
    if not get_review:
        raise error.NotFoundError("Review does not exist")
    await review_repo.delete(get_review.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
