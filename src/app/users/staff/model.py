from lib.db.primary_key import sa, Base
from sqlalchemy.orm import relationship
from lib.utils.random_string import random_str
from src.app.users.staff.staff_ass import staff_permission_association_table


class Staff(Base):
    __tablename__ = "staff"
    aud = sa.Column(sa.String(8), default=lambda: f"st-{random_str(5)}")
    user_id = sa.Column("User", sa.ForeignKey("user.id", ondelete="SET NULL"))
    user = relationship("User", back_populates="staff")
    permissions = relationship(
        "Permission", secondary=staff_permission_association_table
    )
