# import all apps model to this file for alembic migration access
from src.app.users.customer.model import Customer
from src.app.users.staff.model import Staff
from src.app.users.permission.model import Permission
from src.app.auth.model import AuthToken
from src.app.product.category.model import ProductCategory
from src.app.product.measuring_unit.model import ProductMeasuringUnit
from src.app.product.promo_code.model import ProductPromoCode
from src.app.product.medias.model import ProductMedia
from src.app.product.product.model import Product

model_for_alembic = [
    Customer,
    Staff,
    Permission,
    AuthToken,
    ProductPromoCode,
    ProductMeasuringUnit,
    ProductCategory,
    ProductMedia,
    Product,
]
