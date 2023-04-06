from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa


class ProductCategory(Base):
    __tablename__ = "product_category"
    name = sa.Column(sa.String(24))

    def __init__(self, name: str) -> None:
        self.name = name
