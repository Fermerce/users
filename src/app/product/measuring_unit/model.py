from src.lib.db.primary_key import Base, sa


class ProductMeasuringUnit(Base):
    __tablename__ = "product_measuring_unit"
    unit = sa.Column(sa.String(24))

    def __init__(self, unit: str) -> None:
        self.unit = unit
