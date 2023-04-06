import ormar
from lib.db import model


class ProductCategory(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "p_category"

    name: str = ormar.String(max_length=20)
