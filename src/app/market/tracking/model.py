from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship


class Tracking(Base):
    __tablename__ = "order_tracking"
    order_id = sa.Column(GUID, sa.ForeignKey("order.id", ondelete="CASCADE"))
    order = relationship("Order", back_populates="trackings")
    location = sa.Column(sa.String(50))
    note = sa.Column(sa.String(300), nullable=True)
