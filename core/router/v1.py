from fastapi import APIRouter
from lib.utils import get_api_prefix
from src.app.users.user.api.v1 import router as users_api_router
from src.app.users.staff.api.v1 import router as staff_api_router
from src.app.product.category.api.v1 import router as category_api_router
from src.app.market.country.api.v1 import router as country_api_router
from src.app.market.state.api.v1 import router as state_api_router
from src.app.product.measuring_unit.api.v1 import router as measurement_unit_api_router
from src.app.product.promo_code.api.v1 import router as promotion_code_api_router
from src.app.market.status.api.v1 import router as status_api_router
from src.app.market.order.api.v1 import router as order_api_router
from src.app.market.tracking.api.admin_v1 import router as tracking_api_router

router = APIRouter(prefix=get_api_prefix.get_prefix())
router.include_router(router=users_api_router)
router.include_router(router=staff_api_router)
router.include_router(router=country_api_router)
router.include_router(router=state_api_router)
router.include_router(router=status_api_router)
router.include_router(router=category_api_router)
router.include_router(router=measurement_unit_api_router)
router.include_router(router=promotion_code_api_router)
