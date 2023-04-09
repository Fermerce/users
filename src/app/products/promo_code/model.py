import datetime
from lib.db.primary_key import Base, sa, GUID
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import product_promo_codes_table


class ProductPromoCode(Base):
    __tablename__ = "product_promo_code"
    code = sa.Column(sa.String(10))
    discount = sa.Column(sa.Float, nullable=False, default=10.0)
    single = sa.Column(sa.Boolean, default=False)
    active_from = sa.Column(
        sa.DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.datetime.utcnow(),
    )
    active_to = sa.Column(
        sa.DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.datetime.utcnow(),
    )
    products = relationship("Product", secondary=product_promo_codes_table)
    owner_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="promo_codes")
