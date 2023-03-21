import typing as t
from src.app.permission.model import Permission
from src.lib.base.repository import BaseRepository
from src.lib.errors import error
from src.app.user import model, schema


class UserRepository(BaseRepository[model.User]):
    def __init__(self):
        super().__init__(model.User)

    async def create(self, obj: schema.IRegister) -> model.User:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.User.generate_hash(obj.password.get_secret_value())
        new_user = dict(**obj.dict(exclude={"password"}), password=new_password)

        return await super().create(new_user)

    async def update(self, user: model.User, obj: schema.IRegister) -> model.User:
        check_user: model.User = await super().get(user.id)
        if check_user:
            for k, v in obj.dict().items():
                if hasattr(check_user, k):
                    setattr(check_user, k, v)
        if obj.password:
            check_user.hash_password()
        self.db.add(check_user)
        await self.db.commit()
        return check_user

    async def add_user_permission(
        self,
        user_id: str,
        perm_objs: t.List[Permission],
    ) -> model.User:
        user = await super().get(user_id, load_related=True)
        if user is None:
            raise error.NotFoundError("User not found")
        existed_perms = set()
        for permission in perm_objs:
            for per in user.permissions:
                if per.name == permission.name:
                    existed_perms.add(permission.name)
                    perm_objs.pop(perm_objs.index(permission))
        if len(existed_perms) > 0:
            raise error.DuplicateError(
                f"`{','.join(existed_perms)}`permissions already exists for user {user.firstname} {user.lastname}"
            )
        self.db.expunge(user)

        user.permissions.extend(perm_objs)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def remove_user_permission(
        self,
        user_id: str,
        perm_objs: t.List[Permission],
    ) -> model.User:
        user = await super().get(user_id, load_related=True)
        if user is None:
            raise error.NotFoundError("User not found")
        if len(user.permissions) == 0:
            raise error.NotFoundError("User has no permissions")
        for permission in perm_objs:
            for perm in user.permissions:
                if not perm.name == permission.name:
                    raise error.DuplicateError(
                        f"Permission `{perm.name }` not found for user {user.firstname} {user.lastname}"
                    )
                user.permissions.remove(perm)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> model.User:
        user = await super().get_by_attr(attr=dict(email=email), first=True)
        return user

    async def update_password(
        self, user: model.User, obj: schema.IResetPassword
    ) -> model.User:
        user.password = obj.password.get_secret_value()
        user.hash_password()
        self.db.add(user)
        await self.db.commit()
        return user

    async def activate(self, user: model.User, mode: bool = True) -> model.User:
        user.is_active = mode
        self.db.add(user)
        await self.db.commit()
        return user

    async def delete(self, user: model.User, permanent: bool = False) -> model.User:
        if permanent:
            await super().delete(user.id)
            return True
        return await self.activate(user)


user_repo = UserRepository()
