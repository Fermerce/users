import ormar
from lib.db import model


class ProductMedia(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "product_media"

    alt = ormar.String(max_length=225)
    url = ormar.String(max_length=225)
    content_type = ormar.String(max_length=30)
