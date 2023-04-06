import ormar
from lib.db import model


class ProductPromoCode(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "p_promocode"

    code = ormar.String(max_length=10)
