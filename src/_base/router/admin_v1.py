from fastapi import APIRouter
from src.lib.utils import get_api_prefix
from src.app.users.customer.api.admin_v1 import router as customer_api_router
from src.app.users.permission.api.v1 import router as permission_api_router
from src.app.users.staff.api.admin_v1 import router as staff_api_router

router = APIRouter(prefix=f"{get_api_prefix.get_prefix()}")
router.include_router(router=permission_api_router)
router.include_router(router=customer_api_router)
router.include_router(router=staff_api_router)
