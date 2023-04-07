import datetime
from lib.db.primary_key import Base, sa, GUID
from sqlalchemy.orm import relationship


class ProductPromoCode(Base):
    __tablename__ = "product_promo_code"
    code = sa.Column(sa.String(10))
    discount = sa.Column(sa.Float, nullable=False, default=10.0)
    start = sa.Column(sa.DateTime, default=lambda: datetime.datetime.utcnow())
    end = sa.Column(sa.DateTime, default=lambda: datetime.datetime.utcnow())
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="promo_codes")
