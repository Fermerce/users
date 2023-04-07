from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from lib.utils.password_hasher import Hasher
from lib.utils.random_string import random_str
from src.app.users.user.abstract import BaseUser


staff_role_association_table = sa.Table(
    "staff_role_association",
    Base.metadata,
    sa.Column(
        "staff_id",
        sa.ForeignKey(
            "staff.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        sa.ForeignKey(
            "permission.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)


class Staff(BaseUser):
    __tablename__ = "staff"
    aud = sa.Column(sa.String(8), default=lambda: f"ST-{random_str(5)}")
    password_reset_token = sa.Column(sa.String, default=None)
    tel = sa.Column(sa.String(17))
    permissions = relationship(
        "Permission",
        secondary=staff_role_association_table,
        back_populates="staff",
    )

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
