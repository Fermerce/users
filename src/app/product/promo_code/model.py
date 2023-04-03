from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa


class ProductPromoCode(Base):
    __tablename__ = "product_promo_code"
    code = sa.Column(sa.String(10))

    def __init__(self, code: str) -> None:
        self.code = code
