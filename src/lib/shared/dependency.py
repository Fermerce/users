import typing as t
import jose
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src._base.repository.base import BaseRepository
from src.app.permission.model import Permission
from src.lib.errors import error
from src._base.settings import config as base_config
from src.lib.utils import get_api_prefix
from src.lib.db.primary_key import Base


Oauth_schema = OAuth2PasswordBearer(tokenUrl=f"{get_api_prefix.get_prefix()}/auth/login")


class AppAuth:
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


ModelType = t.TypeVar("ModelType", bound=Base)


class AppWrite(t.Generic[ModelType]):
    def __init__(self, model: ModelType, model_repo: BaseRepository) -> None:
        self.model = model
        self.repo = model_repo

    async def get_user_data(
        self, user_id: str, load_related: bool = False
    ) -> t.Union[ModelType, None]:
        if user_id:
            get_user = await self.repo.get(id=user_id, load_related=load_related)
            if get_user and get_user.is_verified:
                return get_user
            raise error.ForbiddenError("Authorization failed")
        return error.UnauthorizedError("Authorization failed")

    async def get_permissions(
        self, db_column_name: str = "permissions", user_id: str = None
    ) -> ModelType:
        check_user: ModelType = await self.get_user_data(user_id=user_id, load_related=True)
        if not check_user:
            raise error.UnauthorizedError("Authorization failed")
        if hasattr(check_user, db_column_name):
            permissions: t.List[Permission] = getattr(check_user, db_column_name)
            if not permissions:
                raise error.AccessDenied()
            return check_user
        raise error.AccessDenied()

    async def require_permission(
        self, permissions: t.List[str], db_column_name: str = "permissions", user_id: str = None
    ) -> t.Union[ModelType, None]:
        check_user = await self.get_user_data(user_id=user_id, load_related=True)

        if not check_user:
            raise error.UnauthorizedError("Authorization failed")
        if hasattr(check_user, db_column_name):
            permission_names: t.List[str] = [
                perm.name for perm in getattr(check_user, db_column_name)
            ]
            if not [name for name in permission_names if name in permissions]:
                raise error.AccessDenied()
            return check_user
        raise error.AccessDenied()

    async def current_user_with_data(self, user_id: str = None):
        if not user_id:
            raise error.UnauthorizedError("Authorization failed")
        active_user: ModelType = await self.get_user_data(user_id=user_id, load_related=True)
        if active_user:
            return active_user
        raise error.UnauthorizedError("Authorization failed")

    async def current_user(self, user_id: str = None):
        user: ModelType = await self.get_user_data(user_id=user_id)

        if user:
            return user
        raise error.UnauthorizedError("Authorization failed")
