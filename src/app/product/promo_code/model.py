from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa
from src.app.product.product.associate_model import product_promo_code_association_table


class ProductPromoCode(Base):
    __tablename__ = "product_promo_code"
    code = sa.Column(sa.String(10))
    products = relationship(
        "Product",
        secondary=product_promo_code_association_table,
        back_populates="promo_codes",
    )
