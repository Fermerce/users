import uuid
from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa


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
        default=lambda: f"PR-{str(uuid.uuid4()).split('-')[-1].upper()}",
        unique=True,
    )
    # medias = Set("ProductMedia")
    # product_categorys = Set("ProductCategory")
    # product_detail = Required("ProductDetail")
    # product_promo_code = Optional("ProductPromoCode")
    # carts = Set("Cart")
    # product_types = Set("Country")
    # order_items = Set("OrderItem")
    # sales_mode = Set("ProductMeasurement")
    # reviews = Set("ProductReview")
    # store = Optional("VendorStore")
    # vendor = Required("Vendor")
