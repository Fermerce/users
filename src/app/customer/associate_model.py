from src.lib.db.primary_key import Base, sa


customer_permission_association_table = sa.Table(
    "customer_role_association",
    Base.metadata,
    sa.Column(
        "customer_id",
        sa.ForeignKey("customer.id"),
        primary_key=True,
        onupdate="CASCADE",
    ),
    sa.Column(
        "permission_id",
        sa.ForeignKey("permission.id"),
        primary_key=True,
        onupdate="SET NULL",
    ),
)
