import typing as t
from sqlalchemy import select, func

from src.app.products.product.model import Product
from src.app.users.user.model import User
from core.repository.base import BaseRepository
from src.app.market.reviews import model


class ReviewRepository(BaseRepository[model.Review]):
    def __init__(self):
        super().__init__(model.Review)

    async def get_by_user(
        self, user: User, per_page: int = 10, page: int = 1
    ) -> t.Tuple[t.List[model.Review], int]:
        stm = (
            select(self.model)
            .filter_by(user=user)
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        result = await self.db.execute(stm)
        return result.scalars().all(), len(result.scalars().all())

    async def get_by_product(
        self, product: Product, per_page: int = 10, page: int = 1
    ) -> t.Tuple[t.List[model.Review], int]:
        stm = (
            select(self.model)
            .filter_by(product=product)
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        result = await self.db.execute(stm)
        return result.scalars().all(), len(result.scalars().all())

    async def get_average_rating(self, product) -> float:
        stmt = select(func.avg(self.model.rating)).where(self.model.product == product)
        average_rating = await self.db.execute(stmt).scalar()
        rounded_rating = round(average_rating, 2)
        return rounded_rating


review_repo = ReviewRepository()
