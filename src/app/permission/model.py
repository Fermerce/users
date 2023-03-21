from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa
from src.app.user.associate_model import user_to_permissions_association_table


class Permission(Base):
    __tablename__ = "permission"
    name = sa.Column(sa.String(24))
    users = relationship(
        "User",
        secondary=user_to_permissions_association_table,
        back_populates="permissions",
    )

    def __init__(self, name: str) -> None:
        self.name = name
