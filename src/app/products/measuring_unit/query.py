from core.query.base_query import BaseQuery
from src.app.products.measuring_unit import model


class ProductMeasuringUnitQuery(BaseQuery[model.ProductMeasuringUnit,]):
    def __init__(self):
        super().__init__(model.ProductMeasuringUnit)


product_measuring_unit_query = ProductMeasuringUnitQuery()
