from lib.db.primary_key import Base, sa


class State(Base):
    __tablename__ = "state"
    name = sa.Column(sa.String(24))

    def __init__(self, name: str) -> None:
        self.name = name
