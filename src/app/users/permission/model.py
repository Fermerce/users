from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa
from src.app.users.user.model import users_permission_association_table


class Permission(Base):
    __tablename__ = "permission"
    name = sa.Column(sa.String(24))
    users = relationship(
        "User",
        secondary=users_permission_association_table,
        back_populates="permissions",
    )

    def __init__(self, name: str) -> None:
        self.name = name
