import typing as t
import uuid
import pydantic as pyd
from src.app.products.product import schema as product_schema


class ICartIn(pyd.BaseModel):
    quantity: int = 1
    product_id: uuid.UUID


class ICartOut(pyd.BaseModel):
    id: uuid.UUID
    quantity: int = 1
    # product: product_schema.IProductShortInfo

    class Config:
        orm_mode = True
