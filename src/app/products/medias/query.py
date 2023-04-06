from core.query.base_query import BaseQuery
from src.app.products.medias import model


class ProductMediaQuery(BaseQuery[model.ProductMedia]):
    def __init__(self):
        super().__init__(model.ProductMedia)


product_media_query = ProductMediaQuery()
