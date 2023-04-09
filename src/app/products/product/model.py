import uuid
from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa, GUID
from src.app.products.product.association_model import (
    product_category_association_table,
    product_promo_codes_table,
    product_measuring_unit_association_table,
    product_country_association_table,
    product_state_association_table,
    product_media_table,
)


class ProductDetail(Base):
    __tablename__ = "product_detail"

    title = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    product_id = sa.Column(GUID, sa.ForeignKey("product.id"))
    product = relationship("Product", back_populates="details")


class Product(Base):
    __tablename__ = "product"
    name = sa.Column(sa.String(50), nullable=False)
    slug = sa.Column(sa.String(70), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    price = sa.Column(sa.Numeric(precision=10, decimal_return_scale=2), nullable=False)
    in_stock = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    sku = sa.Column(
        sa.String(25),
        default=lambda: f"PR-{str(uuid.uuid4()).split('-')[-1]}",
        unique=True,
    )
    medias = relationship("Media", secondary=product_media_table)
    categories = relationship(
        "ProductCategory", secondary=product_category_association_table
    )
    measurement_units = relationship(
        "ProductMeasurement", secondary=product_measuring_unit_association_table
    )
    promo_codes = relationship("ProductPromoCode", secondary=product_promo_codes_table)
    details = relationship("ProductDetail", back_populates="product")
    carts = relationship("Cart", back_populates="product")
    country = relationship("Country", secondary=product_country_association_table)
    state = relationship("State", secondary=product_state_association_table)
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("ProductReview", back_populates="product")
    vendor = relationship("Vendor", back_populates="products", uselist=False)
