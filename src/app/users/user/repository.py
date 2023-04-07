import typing as t
from core.repository.base import BaseRepository
from src.app.users.permission.model import Permission
from lib.errors import error
from src.app.users.user import model, schema


class UserRepository(BaseRepository[model.User]):
    def __init__(self):
        super().__init__(model.User)

    async def create(self, obj: schema.IUserIn) -> model.User:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.User.generate_hash(obj.password.get_secret_value())
        new_customer = dict(**obj.dict(exclude={"password"}), password=new_password)

        return await super().create(new_customer)

    async def update(
        self, user: model.User, obj: t.Union[schema.IUserIn, dict]
    ) -> model.User:
        if user:
            if isinstance(obj, schema.IUserIn):
                for k, v in obj.dict().items():
                    if hasattr(user, k):
                        setattr(user, k, v)
                if obj.password:
                    user.password = user.generate_hash(obj.get("password"))
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    if hasattr(user, k):
                        setattr(user, k, v)
                if obj.get("password", None):
                    user.password = user.generate_hash(obj.get("password"))
        self.db.add(user)
        await self.db.commit()
        return user

    async def add_users_permission(
        self,
        users_id: str,
        permission_objs: t.List[Permission],
    ) -> model.User:
        user = await super().get(users_id, load_related=True, expunge=True)
        if user is None:
            raise error.NotFoundError(" user not found")
        existed_perms = set()
        for permission in permission_objs:
            for per in user.permissions:
                if per.name == permission.name:
                    existed_perms.add(permission.name)
                    permission_objs.pop(permission_objs.index(permission))
        if len(existed_perms) > 0:
            raise error.DuplicateError(
                f"`{','.join(existed_perms)}`role/roles already exists"
            )

        user.permissions.extend(permission_objs)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def remove_users_permission(
        self,
        users_id: str,
        permission_objs: t.List[Permission],
    ) -> model.User:
        user = await super().get(users_id, load_related=True, expunge=False)
        if user is None:
            raise error.NotFoundError(" user not found")
        if len(user.permissions) == 0:
            raise error.NotFoundError(" user has no permissions")
        for permission in permission_objs:
            for per in user.permissions:
                if not per.name == permission.name:
                    raise error.DuplicateError(
                        f"role `{permission.name }` not found for  user { user.firstname} { user.lastname}"
                    )
        user.permissions.remove(per)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> model.User:
        user = await super().get_by_attr(attr=dict(email=email), first=True)
        return user

    async def update_password(
        self, user: model.User, obj: schema.IUserResetPassword
    ) -> model.User:
        str_pass = obj.password.get_secret_value()
        user.password = user.generate_hash(str_pass)
        self.db.add(user)
        await self.db.commit()
        return user

    async def activate(self, user: model.User, mode: bool = True) -> model.User:
        user.is_active = mode
        user.is_verified = mode
        user.is_suspended = mode
        self.db.add(user)
        await self.db.commit()
        return user

    async def delete(self, user: model.User, permanent: bool = False) -> model.User:
        if permanent:
            await super().delete(id=str(user.id))
            return True
        return await self.activate(user, mode=permanent)


users_repo = UserRepository()
