import datetime
from lib.db.primary_key import Base, sa


class ProductCategory(Base):
    __tablename__ = "product_category"
    name = sa.Column(sa.String(24))
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
