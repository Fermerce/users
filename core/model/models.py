# import all apps model to this file for alembic migration access
from src.app.users.user.model import User
from src.app.users.staff.model import Staff
from src.app.users.permission.model import Permission
from src.app.auth.model import AuthToken
from src.app.product.type.model import Country
from src.app.product.category.model import ProductCategory
from src.app.product.measuring_unit.model import ProductMeasuringUnit
from src.app.product.promo_code.model import ProductPromoCode
from src.app.product.category.model import ProductCategory
from src.app.market.status.model import Status

model_for_alembic = [
    User,
    Staff,
    Permission,
    AuthToken,
    ProductPromoCode,
    ProductMeasuringUnit,
    Country,
    ProductCategory,
    Status,
]
