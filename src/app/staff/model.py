from src.lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship
from src.lib.utils.password_hasher import Hasher
from src.app.staff.associate_model import staff_role_association_table
from src.lib.utils.random_string import random_str


class Staff(Base):
    __tablename__ = "staff"
    aud = sa.Column(sa.String(8), default=lambda: f"ST-{random_str(5)}")
    firstname = sa.Column(sa.String(20))
    lastname = sa.Column(sa.String(20))
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String)
    is_verified = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=False)
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
