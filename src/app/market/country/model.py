from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import product_country_association_table
from src.app.vendors.vendor.model import vendor_country_association


class Country(Base):
    __tablename__ = "country"
    name = sa.Column(sa.String(24))
    products = relationship("Product", secondary=product_country_association_table)
    vendors = relationship("Vendor", secondary=vendor_country_association)
