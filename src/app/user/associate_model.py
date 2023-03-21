from src.lib.db.primary_key import Base, sa


user_to_permissions_association_table = sa.Table(
    "user_permissions_association",
    Base.metadata,
    sa.Column(
        "user_id",
        sa.ForeignKey("user.id"),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        sa.ForeignKey("permission.id"),
        primary_key=True,
    ),
)
