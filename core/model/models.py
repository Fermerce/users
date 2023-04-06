# import all apps model to this file for alembic migration access
from src.app.users.customer.model import Customer
from src.app.users.staff.model import Staff
from src.app.users.permission.model import Permission
from src.app.users.auth.model import AuthToken
from src.app.products.product.model import Product
from src.app.products.category.model import ProductCategory
from src.app.products.measuring_unit.model import ProductMeasuringUnit
from src.app.products.promo_code.model import ProductPromoCode
from src.app.products.medias.model import ProductMedia
from src.app.products.product.model import ProductDetail

model_for_alembic = [
    Customer,
    Staff,
    Permission,
    AuthToken,
    Product,
    ProductPromoCode,
    ProductMeasuringUnit,
    ProductCategory,
    ProductMedia,
    ProductDetail,
]
