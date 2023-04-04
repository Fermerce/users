import uuid
from src.lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship
from src.app.product.product.associate_model import (
    product_category_association_table,
    product_promo_code_association_table,
    product_measure_unit_association_table,
)
from src.lib.utils.random_string import generate_orderId


class Product(Base):
    __tablename__ = "product"
    name = sa.Column(sa.String(50))
    slug = sa.Column(sa.String)
    stock_unit = sa.Column(sa.Integer, default=1)
    original_price = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)
    sale_price = sa.Column(sa.Numeric(precision=10, scale=2))
    discount = sa.Column(sa.Float, default=0.0)
    sku = sa.Column(sa.String(16), default=lambda: generate_orderId(12))
    description = sa.Column(sa.Text)
    is_series = sa.Column(sa.Boolean, default=False)
    in_stock = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    details = relationship("ProductDetail", back_populates="product")
    measuring_units = relationship(
        "ProductMeasuringUnit",
        secondary=product_measure_unit_association_table,
        back_populates="products",
    )
    promo_codes = relationship(
        "ProductPromoCode",
        secondary=product_promo_code_association_table,
        back_populates="products",
    )
    categories = relationship(
        "ProductCategory",
        secondary=product_category_association_table,
        back_populates="products",
    )
    medias = relationship(
        "ProductMedia",
        back_populates="product",
    )


class ProductDetail(Base):
    __tablename__ = "product_detail"
    title = sa.Column(sa.String(50))
    detail = sa.Column(sa.Text)
    product_id = sa.Column(GUID, sa.ForeignKey("product.id"))
    product = relationship("Product", back_populates="details")
