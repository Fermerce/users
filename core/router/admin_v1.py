from fastapi import APIRouter
from lib.utils import get_api_prefix
from src.app.users.user.api.admin_v1 import router as users_api_router
from src.app.users.permission.api.v1 import router as permission_api_router
from src.app.users.staff.api.v1 import router as staff_api_router
from src.app.market.status.api.admin_v1 import router as status_api_router

router = APIRouter(prefix=f"{get_api_prefix.get_prefix()}")
router.include_router(router=permission_api_router)
router.include_router(router=users_api_router)
router.include_router(router=staff_api_router)
router.include_router(router=status_api_router)
