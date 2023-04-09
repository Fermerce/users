from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship


class Cart(Base):
    __tablename__ = "cart"
    quantity = sa.Column(sa.Integer, default=1)
    product_id = sa.Column(
        GUID, sa.ForeignKey("product.id", ondelete="SET NULL"), nullable=False
    )
    product = relationship("Product", back_populates="carts")
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="carts")
