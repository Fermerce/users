from core.query.base_query import BaseQuery
from src.app.products.category import model


class ProductCategoryQuery(BaseQuery[model.ProductCategory,]):
    def __init__(self):
        super().__init__(model.ProductCategory)


product_category_query = ProductCategoryQuery()
