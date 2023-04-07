from lib.db.primary_key import GUID, Base, sa
from sqlalchemy.orm import relationship
from lib.utils.random_string import generate_orderId


class Payment(Base):
    __tablename__ = "payments"
    reference = sa.Column(sa.String(18), default=lambda: generate_orderId(15))
    total = sa.Column(sa.Numeric(precision=10, scale=2))
    promo_code_id = sa.Column(GUID, sa.ForeignKey("product_promo_code.id", ondelete="SET NULL"), nullable=False)
    promo_code = relationship("Product", foreign_keys=[promo_code_id])
    user_id = sa.Column(GUID, sa.ForeignKey("user.id", ondelete="SET NULL"))
    user = relationship("User", related_name="payments")
    status_id = sa.Column(GUID, sa.ForeignKey("status.id", ondelete="SET NULL"))
    status = relationship("Status", foreign_keys=[status_id], uselist=False)
    order = relationship("Order", back_populates="payment", uselist=False)
