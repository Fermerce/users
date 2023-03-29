from src.lib.db.primary_key import Base, sa


staff_role_association_table = sa.Table(
    "staff_role_association",
    Base.metadata,
    sa.Column(
        "staff_id",
        sa.ForeignKey(
            "staff.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        sa.ForeignKey(
            "permission.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)
