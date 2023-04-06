import ormar
from lib.db import model


class ProductMeasuringUnit(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "product_measuring_unit"

    unit = ormar.String(max_length=24)
