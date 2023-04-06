import ormar
from lib.db import model


class AuthToken(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "auth_token"

    refresh_token: str = ormar.String(max_length=255, nullable=True)
    access_token: str = ormar.String(max_length=255, nullable=True)
    aud: str = ormar.UUID(uuid_format="string")
    ip_address: str = ormar.String(max_length=24)
