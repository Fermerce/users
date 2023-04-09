from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship


class ShippingAddress(Base):
    __tablename__ = "shipping_address"
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="shipping_address")
    orders = relationship("Order", back_populates="shipping_address")
    street = sa.Column(sa.String(100))
    phones = sa.Column(sa.String(500))
    city = sa.Column(sa.String(100))
    state = sa.Column(sa.String(100))
    zipcode = sa.Column(sa.String(10))
