from sqlalchemy.orm import relationship
from src.lib.db.primary_key import Base, sa, GUID


class ProductMedia(Base):
    __tablename__ = "product_media"
    alt = sa.Column(sa.String(225))
    url = sa.Column(sa.String(225))
    content_type = sa.Column(sa.String(30))
    product_id = sa.Column(GUID, sa.ForeignKey("product.id"))
    product = relationship("Product", back_populates="medias")
