from fastapi import APIRouter
from src.lib.utils import get_api_prefix
from src.app.customer.api.v1 import router as customer_api_router
from src.app.staff.api.v1 import router as staff_api_router
from src.app.auth.api.v1 import router as auth_api_router

router = APIRouter(prefix=get_api_prefix.get_prefix())
router.include_router(router=auth_api_router)
router.include_router(router=customer_api_router)
router.include_router(router=staff_api_router)
