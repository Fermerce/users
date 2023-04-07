import typing as t
from uuid import UUID
import sqlalchemy as sa
from lib.errors import error
from src.app.products.product.model import Product
from src.app.users.user.model import User
from core.repository.base import BaseRepository
from src.app.market.cart import model, schema


class CartRepository(BaseRepository[model.Cart]):
    def __init__(self):
        super().__init__(model.Cart)

    async def get_user_cart(self, user: User) -> t.List[model.Cart]:
        return await super().get_by_attr(attr={"user", user})

    async def get_cart_by_ids(
        self,
        user: User,
        cart_ids: t.Optional[t.List[UUID]] = None,
    ) -> t.Optional[t.List[model.Cart]]:
        if cart_ids is not None:
            stm = (
                sa.select(self.model)
                .options(sa.orm.selectinload("*"))
                .where(self.model.id.in_(cart_ids), self.model.user == user)
            )
            result = await self.db.execute(stm)
            return result.scalars().all()
        stm = sa.select(self.model).where(self.model.user == user)
        result = await self.db.execute(stm)
        return result.scalars().all()

    async def create(
        self,
        obj: schema.ICartIn,
        user: User,
        product: Product,
    ) -> model.Cart:
        if not product:
            raise error.NotFoundError("Product not found")
        new_cart = await super().create(
            dict(
                pdf=obj.pdf,
                paper_back_qty=obj.paper_back_qty,
                hard_back_qty=obj.hard_back_qty,
                user=user,
                item=product,
            )
        )
        return new_cart

    async def update(self, obj: schema.ICartIn, cart_id: UUID) -> model.Cart:
        cart = await super().update(cart_id, obj.dict(exclude={"product_id"}))
        if not cart:
            raise error.NotFoundError("Product not found")
        return cart


cart_repo = CartRepository()
