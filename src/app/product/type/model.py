from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa


class ProductType(Base):
    __tablename__ = "product_type"
    name = sa.Column(sa.String(24))

    def __init__(self, name: str) -> None:
        self.name = name
