from src.lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.lib.utils.password_hasher import Hasher
from src.app.customer.associate_model import customer_permission_association_table
from src.lib.utils.random_string import random_str


class Customer(Base):
    __tablename__ = "customer"
    firstname = sa.Column(sa.String(20), nullable=True)
    lastname = sa.Column(sa.String(20), nullable=True)
    username = sa.Column(sa.String(30), default=lambda: f"FM-{random_str(5)}")
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String)
    password_reset_token = sa.Column(sa.String, default=None)
    permissions = relationship(
        "Permission",
        secondary=customer_permission_association_table,
        back_populates="customers",
    )
    is_verified = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=True)

    @staticmethod
    def generate_hash(password: str) -> str:
        return Hasher.hash_password(password)

    def check_password(self, plain_password: str) -> bool:
        check_pass = Hasher.check_password(plain_password, self.password)
        if check_pass:
            return True
        return False
