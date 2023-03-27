from fastapi import Depends
from src.lib.shared.dependency import AppAuth, AppWrite
from src.app.customer.model import Customer
from src.app.customer.repository import customer_repo

__customer_write = AppWrite(model=Customer, model_repo=customer_repo)


async def require_customer(get_user: dict = Depends(AppAuth.authenticate)):
    return await __customer_write.get_user_data(user_id=get_user.get("user_id", None))
