from lib.db.primary_key import sa
from sqlalchemy.orm import relationship
from lib.utils.password_hasher import Hasher
from src.app.users.user.abstract import BaseUser


class User(BaseUser):
    __tablename__ = "user"
    reset_token = sa.Column(sa.String, default=None)
    staff = relationship("Staff", back_populates="user", uselist=False)
    carts = relationship("Cart", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    orders = relationship("Order", back_populates="user")
    vendor = relationship("Vendor", back_populates="user")
    shipping_address = relationship("ShippingAddress", back_populates="user")

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
