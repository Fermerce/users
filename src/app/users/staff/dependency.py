from fastapi import Depends
from src.lib.shared.dependency import AppAuth, AppWrite
from src.app.users.staff.model import Staff
from src.app.users.staff.repository import staff_repo

__staff_write = AppWrite(model=Staff, model_repo=staff_repo)


async def get_permissions(get_user: dict = Depends(AppAuth.authenticate)):
    data = await __staff_write.get_permissions(
        db_column_name="permissions", user_id=get_user.get("user_id", None)
    )
    return data


async def require_admin(get_user: dict = Depends(AppAuth.authenticate)):
    data = await __staff_write.require_permission(
        permissions=["admin"],
        db_column_name="permissions",
        user_id=get_user.get("user_id", None),
    )
    return data


async def require_super_admin(get_user: dict = Depends(AppAuth.authenticate)):
    data = await __staff_write.require_permission(
        permissions=["super_admin"],
        db_column_name="permissions",
        user_id=get_user.get("user_id", None),
    )
    return data


async def require_super_admin_or_admin(get_user: dict = Depends(AppAuth.authenticate)):
    await __staff_write.require_permission(
        permissions=["super_admin", "admin"],
        db_column_name="permissions",
        user_id=get_user.get("user_id", None),
    )


async def require_dispatcher(get_user: dict = Depends(AppAuth.authenticate)):
    await __staff_write.require_permission(
        permissions=["dispatcher"],
        db_column_name="permissions",
        user_id=get_user.get("user_id", None),
    )


async def require_staff_data_all(get_user: dict = Depends(AppAuth.authenticate)):
    data = await __staff_write.current_user_with_data(
        user_id=get_user.get("user_id", None)
    )
    return data


async def require_staff_data(get_user: dict = Depends(AppAuth.authenticate)):
    data = await __staff_write.current_user(user_id=get_user.get("user_id", None))
    return data
