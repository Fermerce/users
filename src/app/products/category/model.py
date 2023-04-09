from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import (
    product_category_association_table,
)


class ProductCategory(Base):
    __tablename__ = "product_category"
    name = sa.Column(sa.String(24))
    product = relationship("Product", secondary=product_category_association_table)
