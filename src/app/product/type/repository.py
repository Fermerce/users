from src._base.repository.base import BaseRepository
from src.app.product.type import model


class ProductTypeRepository(BaseRepository[model.ProductType,]):
    def __init__(self):
        super().__init__(model.ProductType)


product_type_repo = ProductTypeRepository()
