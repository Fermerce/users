from lib.db.primary_key import Base, sa


class Country(Base):
    __tablename__ = "country"
    name = sa.Column(sa.String(24))
