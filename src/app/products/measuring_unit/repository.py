from core.repository.base import BaseRepository
from src.app.products.measuring_unit import model


class ProductMeasuringUnitRepository(BaseRepository[model.ProductMeasuringUnit,]):
    def __init__(self):
        super().__init__(model.ProductMeasuringUnit)


product_measuring_unit_repo = ProductMeasuringUnitRepository()
