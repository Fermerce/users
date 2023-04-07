import datetime
import typing as t
import uuid
import pydantic as pyd
from src.app.market.payment import schema as payment_schema
from src.app.users.address import schema as address_schema
from src.app.users.user import schema as user_schema
from src.app.product.product import schema as product_schema


class IOrderInfo(pyd.BaseModel):
    id: uuid.UUID
    order_id: str
    user: user_schema.IUserOut
    # status: OrderStatus = OrderStatus.PENDING
    shipping_address: address_schema.IAddressOut
    payment: t.Optional[payment_schema.IPaymentOrderOut]
    items: t.List["IOrderItems"] = []
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class IOrderSuccessOut(pyd.BaseModel):
    order_id: str


class IOrderIn(pyd.BaseModel):
    cart_ids: t.Optional[t.List[uuid.UUID]] = None
    address_id: str


class IOrderItemIn(pyd.BaseModel):
    pdf: t.Optional[bool] = True
    paper_back_qty: t.Optional[int] = 0
    hard_back_qty: t.Optional[int] = 0


class IOrderUpdate(pyd.BaseModel):
    order_id: str
    status_id: uuid.UUID


class IOrderItemUpdate(pyd.BaseModel):
    item_tracking_id: str
    delivered: bool = True


class IOrderItems(pyd.BaseModel):
    id: uuid.UUID
    pdf: bool = False
    paper_back_qty: int
    hard_back_qty: int
    delivered: bool = False
    # product: product_schema.IProductShortInfo

    class Config:
        orm_mode = True
