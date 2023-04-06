from fastapi import Depends
from lib.shared.dependency import AppAuth, AppWrite
from src.app.users.customer.model import Customer
from src.app.users.customer.query import customer_query

__customer_write = AppWrite(model=Customer, model_query=customer_query)


async def require_customer(get_user: dict = Depends(AppAuth.authenticate)):
    return await __customer_write.get_user_data(user_id=get_user.get("user_id", None))


async def require_customer_full_data(get_user: dict = Depends(AppAuth.authenticate)):
    return await __customer_write.current_user_with_data(
        user_id=get_user.get("user_id", None)
    )
