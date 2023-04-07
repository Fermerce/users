from lib.db.primary_key import Base, sa
from lib.utils.random_string import random_str


class BaseUser(Base):
    __tablename__ = "user"
    __abstract__ = True
    firstname = sa.Column(sa.String(20), nullable=True)
    lastname = sa.Column(sa.String(20), nullable=True)
    username = sa.Column(sa.String(30), default=lambda: f"FM-{random_str(5)}")
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String)
    is_verified = sa.Column(sa.Boolean, default=False)
    is_suspended = sa.Column(sa.Boolean, default=False)
    is_active = sa.Column(sa.Boolean, default=False)
