from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship


class Cart(Base):
    __tablename__ = "cart"
    quantity = sa.Column(sa.Integer, default=1)
    product_id = sa.Column(GUID, sa.ForeignKey("product.id", ondelete="SET NULL"), nullable=False)
    product = relationship("Product", foreign_keys=[product_id])
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", foreign_keys=[user_id])
