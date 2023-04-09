from sqlalchemy.orm import relationship
from lib.db.primary_key import Base, sa
from src.app.users.staff.model import staff_permission_association_table


class Permission(Base):
    __tablename__ = "permission"
    name = sa.Column(sa.String(24))
    users = relationship("Staff", secondary=staff_permission_association_table)
