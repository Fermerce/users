from fastapi import Depends
from src.lib.shared.dependency import AppAuth, AppWrite
from src.app.customer.model import Customer
from src.app.customer.repository import customer_repo

__staff_write = AppWrite(model=Customer, model_repo=customer_repo)


async def require_customer(get_user: dict = Depends(AppAuth.authenticate)):
    return await __staff_write.get_permissions(
        db_column_name="permissions", user_dict=get_user
    )
    
