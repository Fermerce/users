from src.lib.db.primary_key import Base, sa


staff_role_association_table = sa.Table(
    "staff_role_association",
    Base.metadata,
    sa.Column(
        "staff_id", sa.ForeignKey("staff.id"), primary_key=True, onupdate="CASCADE"
    ),
    sa.Column(
        "permission_id",
        sa.ForeignKey("permission.id"),
        primary_key=True,
        onupdate="SET NULL",
    ),
)
