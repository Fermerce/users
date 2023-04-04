from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa
from src.app.product.product.associate_model import product_category_association_table


class ProductCategory(Base):
    __tablename__ = "product_category"
    name = sa.Column(sa.String(24))
    products = relationship(
        "Product",
        secondary=product_category_association_table,
        back_populates="categories",
    )
