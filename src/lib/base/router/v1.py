from fastapi import APIRouter
from src.lib.utils import get_api_prefix

router = APIRouter(prefix=get_api_prefix.get_prefix())
