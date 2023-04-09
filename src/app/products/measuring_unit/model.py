from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import (
    product_measuring_unit_association_table,
)


class ProductMeasuringUnit(Base):
    __tablename__ = "product_measuring_unit"
    unit = sa.Column(sa.String(24))
    products = relationship(
        "Product", secondary=product_measuring_unit_association_table
    )
