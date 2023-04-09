import typing as t
from core.repository.base import BaseRepository
from src.app.users.user import model, schema


class UserRepository(BaseRepository[model.User]):
    def __init__(self):
        super().__init__(model.User)

    async def create(self, obj: schema.IUserIn) -> model.User:
        for k, _ in obj.dict().items():
            if not hasattr(self.model, k):
                obj.dict().pop(k, None)
        new_password = model.User.generate_hash(obj.password.get_secret_value())
        new_user = dict(**obj.dict(exclude={"password"}), password=new_password)

        return await super().create(new_user)

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
