from lib.db.primary_key import Base, sa


class Status(Base):
    __tablename__ = "status"
    name = sa.Column(sa.String(24))
