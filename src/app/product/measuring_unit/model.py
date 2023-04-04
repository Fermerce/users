from src.lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.product.product.associate_model import (
    product_measure_unit_association_table,
)


class ProductMeasuringUnit(Base):
    __tablename__ = "product_measuring_unit"
    unit = sa.Column(sa.String(24))
    products = relationship(
        "Product",
        secondary=product_measure_unit_association_table,
        back_populates="measuring_units",
    )
