from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa
from src.app.staff.associate_model import staff_role_association_table
from src.app.customer.associate_model import customer_permission_association_table


class Permission(Base):
    __tablename__ = "permission"
    name = sa.Column(sa.String(24))
    staff = relationship(
        "Staff",
        secondary=staff_role_association_table,
        back_populates="permissions",
    )
    customers = relationship(
        "Customer",
        secondary=customer_permission_association_table,
        back_populates="permissions",
    )

    def __init__(self, name: str) -> None:
        self.name = name
