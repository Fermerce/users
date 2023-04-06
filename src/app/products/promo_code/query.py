from core.query.base_query import BaseQuery
from src.app.products.promo_code import model


class ProductPromoCodeQuery(BaseQuery[model.ProductPromoCode,]):
    def __init__(self):
        super().__init__(model.ProductPromoCode)


product_promo_code_query = ProductPromoCodeQuery()
