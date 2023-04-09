from lib.db.primary_key import Base, sa
from sqlalchemy.orm import relationship


class Status(Base):
    __tablename__ = "status"
    name = sa.Column(sa.String(24))
    orders = relationship("Order", back_populates="status")
