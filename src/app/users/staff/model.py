import typing as t
import ormar
from lib.db import model
from lib.utils.password_hasher import Hasher
from lib.utils.random_string import random_str
from src.app.users.permission.model import Permission


class Staff(model.BaseModel):
    class Meta(model.BaseMeta):
        tablename = "staff"

    aud: str = ormar.String(max_length=10, default=lambda: f"ST-{random_str(5)}")
    firstname: str = ormar.String(max_length=20, nullable=True)
    lastname: str = ormar.String(max_length=20, nullable=True)
    username: str = ormar.String(max_length=30, default=lambda: f"FM-{random_str(5)}")
    email: str = ormar.String(max_length=50, unique=True)
    password: str = ormar.String(max_length=300)
    password_reset_token: str = ormar.String(max_length=300, nullable=True)
    is_verified: bool = ormar.Boolean(default=False)
    is_suspended: bool = ormar.Boolean(default=False)
    is_active: bool = ormar.Boolean(default=True)

    tel = ormar.String(max_length=17)
    categories: t.Optional[t.List[Permission]] = ormar.ManyToMany(Permission)

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
