from lib.db.primary_key import sa, Base, GUID
from sqlalchemy.orm import relationship
from src.app.vendors.vendor.vendor_ass import (
    vendor_state_association,
    vendor_country_association,
)


class Vendor(Base):
    __tablename__ = "Vendor"
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    cover_image_id = sa.Column(GUID, nullable=True)
    cover_image = relationship("Media", back_populates="vendors")
    user_id = sa.Column(GUID, sa.ForeignKey("user.id"))
    user = relationship("User", back_populates="Vendor")
    is_verified = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=False)
    states = relationship("State", secondary=vendor_state_association)
    countries = relationship("Country", secondary=vendor_country_association)
    products = relationship("product", back_populates="vendor")
