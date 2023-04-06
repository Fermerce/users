import datetime
import uuid
import ormar
from lib.db import config as db_config


class BaseMeta(ormar.ModelMeta):
    database = db_config.database
    metadata = db_config.metadata


class BaseModel(ormar.Model):
    class Meta:
        abstract = True

    id: uuid.UUID = ormar.UUID(
        primary_key=True, default=uuid.uuid4, uuid_format="string"
    )

    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.utcnow())
    updated_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.utcnow())
