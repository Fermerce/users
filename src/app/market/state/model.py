from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.products.product.association_model import product_state_association_table
from src.app.vendors.vendor.vendor_ass import vendor_state_association


class State(Base):
    __tablename__ = "state"
    name = sa.Column(sa.String(24))
    products = relationship("Product", secondary=product_state_association_table)
    vendors = relationship("Vendor", secondary=vendor_state_association)
