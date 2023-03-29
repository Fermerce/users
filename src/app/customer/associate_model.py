from src.lib.db.primary_key import Base, sa


customer_permission_association_table = sa.Table(
    "customer_role_association",
    Base.metadata,
    sa.Column(
        "customer_id",
        sa.ForeignKey(
            "customer.id",
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
