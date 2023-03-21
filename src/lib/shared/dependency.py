import typing as t
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jose
from src.lib.errors import error
from core.settings import config as base_config
from src.lib.utils import get_api_prefix
from src.app.user.model import User
from src.app.user.repository import user_repo
from src.app.permission.repository import permission_repo


async def get_user_data(
    user_id: str,
    load_related: bool = False,
) -> t.Union[User, None]:
    if user_id:
        get_user: User = await user_repo.get(id=user_id, load_related=load_related)
        if get_user.is_active:
            return get_user
        return None
    return None


async def get_user_permission(user_id: str, name: str) -> t.Union[User, None]:
    if not user_id or not name:
        return None
    get_user = await get_user_data(user_id)
    if not get_user:
        raise error.UnauthorizedError("Authorization failed")
    check_user_perm = await permission_repo.get_by_attr(attr=dict(name=name), first=True)
    if not check_user_perm:
        raise error.NotFoundError("Permission is not available")
    if check_user_perm in get_user.permissions:
        return get_user
    return None


Oauth_schema = OAuth2PasswordBearer(tokenUrl=f"{get_api_prefix.get_prefix()}/auth/login")


class UserAuth:
    @staticmethod
    async def authenticate(
        token: str = Depends(Oauth_schema),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload: dict = jose.jwt.decode(
                token=token,
                key=base_config.secret_key,
                algorithms=[base_config.algorithm],
            )

            if payload is None:
                raise credentials_exception
            if not payload.get("user_id", None):
                raise credentials_exception
            return payload
        except jose.JWTError:
            raise credentials_exception


class UserWrite:
    @staticmethod
    async def is_admin(
        user: dict = Depends(UserAuth.authenticate),
    ) -> User:
        admin_user = await get_user_permission(user_id=user.get("user_id", None), name="admin")
        if admin_user:
            return admin_user
        raise error.ForbiddenError("Authorization failed")

    @staticmethod
    async def is_super_admin(
        user: dict = Depends(UserAuth.authenticate),
    ) -> User:
        super_user = await get_user_permission(
            user_id=user.get("user_id", None),
            name="super_admin",
        )
        if super_user:
            return super_user
        raise error.ForbiddenError("Authorization failed")

    @staticmethod
    async def super_or_admin(
        user: dict = Depends(UserAuth.authenticate),
    ) -> User:
        super_user = await get_user_permission(
            user_id=user.get("user_id", None),
            name="super_admin",
        )
        admin_user = await get_user_permission(user_id=user.get("user_id", None), name="admin")
        if super_user or admin_user:
            return super_user
        raise error.ForbiddenError("Authorization failed")

    @staticmethod
    async def current_user_with_data(
        user: dict = Depends(UserAuth.authenticate),
    ):
        active_user = await get_user_data(user_id=user.get("user_id", None))
        if active_user:
            return active_user
        raise error.UnauthorizedError("Authorization failed")

    @staticmethod
    async def current_user(
        user: dict = Depends(UserAuth.authenticate),
    ):
        user = await get_user_data(user_id=user.get("user_id", None), load_related=True)

        if user:
            return user
        raise error.UnauthorizedError("Authorization failed")
