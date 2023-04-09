from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import product_media_table
from src.app.vendors.vendor.vendor_ass import vendor_media_association


class Media(Base):
    __tablename__ = "media"
    alt = sa.Column(sa.String, unique=True, index=True)
    url = sa.Column(sa.String, unique=True)
    content_type = sa.Column(sa.String(30))
    products = relationship("Product", secondary=product_media_table)
    vendors = relationship("vendor", secondary=vendor_media_association)
