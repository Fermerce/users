from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship


class OrderDeliveryMode(Base):
    __tablename__ = "order_delivery_mode"
    name = sa.Column(sa.String(50))
    price = sa.Column(sa.Numeric(scale=2, precision=12))
    orders = relationship("Order", back_populates="delivery_mode")
