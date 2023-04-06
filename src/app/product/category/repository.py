from core.repository.base import BaseRepository
from src.app.product.category import model


class ProductCategoryRepository(BaseRepository[model.ProductCategory,]):
    def __init__(self):
        super().__init__(model.ProductCategory)


product_category_repo = ProductCategoryRepository()
