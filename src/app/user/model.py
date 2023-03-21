from src.lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.app.user.password_hasher import Hasher
from src.app.user.associate_model import user_to_permissions_association_table


class User(Base):
    __tablename__ = "user"
    firstname = sa.Column(sa.String(20))
    lastname = sa.Column(sa.String(20))
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String)
    permissions = relationship(
        "Permission",
        secondary=user_to_permissions_association_table,
        back_populates="users",
    )
    tel = sa.Column(sa.String(17))
    is_active = sa.Column(sa.Boolean, default=False)

    def hash_password(self) -> str:
        self.password = Hasher.hash_password(self.password)

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
