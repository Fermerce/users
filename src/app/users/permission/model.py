import ormar
from lib.db import model


class Permission(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "permission"

    name: str = ormar.String(max_length=40)
