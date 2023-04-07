from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from lib.utils.password_hasher import Hasher
from lib.utils.random_string import random_str
from src.app.users.user.abstract import BaseUser


users_permission_association_table = sa.Table(
    "users_role_association",
    Base.metadata,
    sa.Column(
        "users_id",
        sa.ForeignKey(
            " user.id",
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


class User(BaseUser):
    __tablename__ = "user"
    password_reset_token = sa.Column(sa.String, default=None)
    orders = relationship("Order", back_populates="user")
    permissions = relationship(
        "Permission",
        secondary=users_permission_association_table,
        back_populates="users",
    )
    payments = relationship("Payment", back_populates="user")
    shipping_address = relationship("ShippingAddress", back_populates="user")
    promo_codes = relationship("ProductPromoCode", back_populates="user")

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
