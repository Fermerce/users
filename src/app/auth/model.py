from src.lib.db.primary_key import Base, sa


class AuthToken(Base):
    __tablename__ = "auth_token"
    refresh_token = sa.Column(sa.String, nullable=True)
    access_token = sa.Column(sa.String, nullable=True)
    user_id = sa.Column(sa.String)
    ip_address = sa.Column(sa.String(24))

    def __init__(
        self,
        user_id: str,
        ip_address: str,
        refresh_token: str = None,
        access_token: str = None,
    ) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.ip_address = ip_address
