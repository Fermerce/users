from fastapi import APIRouter
from src.lib.utils import get_api_prefix
from src.app.users.customer.api.v1 import router as customer_api_router
from src.app.users.staff.api.v1 import router as staff_api_router
from src.app.product.category.api.v1 import router as category_api_router
from src.app.product.type.api.v1 import router as type_api_router
from src.app.product.measuring_unit.api.v1 import router as measurement_unit_api_router
from src.app.product.promo_code.api.v1 import router as promotion_code_api_router

router = APIRouter(prefix=get_api_prefix.get_prefix())
router.include_router(router=customer_api_router)
router.include_router(router=staff_api_router)
router.include_router(router=category_api_router)
router.include_router(router=type_api_router)
router.include_router(router=measurement_unit_api_router)
router.include_router(router=promotion_code_api_router)
