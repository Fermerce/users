from fastapi import APIRouter
from src.lib.utils import get_api_prefix


router = APIRouter(prefix=f"{get_api_prefix.get_prefix()}")
# router.include_router()
