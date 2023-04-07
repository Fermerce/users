from core.repository.base import BaseRepository
from src.app.products.promo_code import model


class ProductPromoCodeRepository(BaseRepository[model.ProductPromoCode,]):
    def __init__(self):
        super().__init__(model.ProductPromoCode)


product_promo_code_repo = ProductPromoCodeRepository()
