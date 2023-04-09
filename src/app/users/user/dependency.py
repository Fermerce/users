from fastapi import Depends
from lib.shared.dependency import AppAuth, AppWrite
from src.app.users.user.model import User
from src.app.users.user.repository import users_repo

__users_write = AppWrite(model=User, model_repo=users_repo)


async def require_user(get_user: dict = Depends(AppAuth.authenticate)):
    return await __users_write.get_user_data(user_id=get_user.get("user_id", None))


async def require_user_full_data(get_user: dict = Depends(AppAuth.authenticate)):
    return await __users_write.current_user_with_data(
        user_id=get_user.get("user_id", None)
    )
