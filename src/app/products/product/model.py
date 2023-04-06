import typing as t
import ormar
from lib.db import model
from lib.utils.random_string import generate_stampId
from src.app.products.measuring_unit.model import ProductMeasuringUnit
from src.app.products.category.model import ProductCategory
from src.app.products.medias.model import ProductMedia
from src.app.products.promo_code.model import ProductPromoCode


class ProductDetail(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "product_detail"

    title: str = ormar.String(max_length=50)
    detail: str = ormar.String(max_length=5000)


class Product(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "product"

    name: str = ormar.String(max_length=50)
    slug: str = ormar.String(max_length=300)
    stock_unit: int = ormar.Integer(default=1)
    original_price: t.Optional[float] = ormar.Float(nullable=True)
    sale_price: float = ormar.Float()
    discount: float = ormar.Float(default=0.0)
    sku: str = ormar.String(max_length=16, default=generate_stampId(12))
    description: str = ormar.String(max_length=5000)
    is_series: bool = ormar.Boolean(default=False)
    in_stock: bool = ormar.Boolean(default=False)
    is_suspended: bool = ormar.Boolean(default=False)

    details: t.List[ProductDetail] = ormar.ForeignKey(
        ProductDetail, related_name="products"
    )

    sales_mode: t.List[ProductMeasuringUnit] = ormar.ManyToMany(
        ProductMeasuringUnit, related_name="products", name="product_mu"
    )

    promo_codes: t.List[ProductPromoCode] = ormar.ManyToMany(
        ProductPromoCode, related_name="products", name="product_code"
    )

    categories: t.List[ProductCategory] = ormar.ManyToMany(
        ProductCategory, related_name="products", name="product_category"
    )

    medias: t.List[ProductMedia] = ormar.ForeignKey(
        ProductMedia, related_name="product"
    )
