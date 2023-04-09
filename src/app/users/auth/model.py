from lib.db.primary_key import Base, sa, GUID


class AuthToken(Base):
    __tablename__ = "auth_token"
    refresh_token = sa.Column(sa.String, nullable=True)
    access_token = sa.Column(sa.String, nullable=True)
    aud = sa.Column(GUID, nullable=False)
    ip_address = sa.Column(sa.String(24))
