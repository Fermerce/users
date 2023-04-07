from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship
from lib.utils.random_string import generate_orderId, random_str


class Order(Base):
    __tablename__ = "order"
    order_id = sa.Column(
        sa.String(15),
        default=lambda: str(generate_orderId(8)),
        index=True,
        unique=True,
    )
    tracking_id = sa.Column(
        sa.String(10),
        default=lambda: str(f"TR-{random_str(7)}"),
        index=True,
        unique=True,
    )
    trackings = relationship("Tracking", back_populates="order")
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="orders")
    shipping_address_id = sa.Column(
        GUID, sa.ForeignKey("shipping_address.id", ondelete="SET NULL")
    )
    shipping_address = relationship("ShippingAddress", back_populates="orders")
    payment_id = sa.Column(GUID, sa.ForeignKey("payment.id", ondelete="CASCADE"))
    payment = relationship("Payment", back_populates="order")
    status_id = sa.Column(
        GUID, sa.ForeignKey("status.id", ondelete="SET NULL"), nullable=True
    )
    status = relationship("Status", foreign_keys=[status_id])
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"
    quantity = sa.Column(sa.Integer, default=0)
    is_delivered = sa.Column(sa.Boolean, default=False)
    product_id = sa.Column(GUID, sa.ForeignKey("product.id"))
    product = relationship("Product", foreign_keys=[product_id])
    order_id = sa.Column(GUID, sa.ForeignKey("order.id", ondelete="CASCADE"))
    order = relationship("Order", back_populates="order")
