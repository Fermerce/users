from src.lib.db.primary_key import Base, sa

product_measure_unit_association_table = sa.Table(
    "product_measuring_unit_association",
    Base.metadata,
    sa.Column(
        "product_measuring_unit_id",
        sa.ForeignKey("product_measuring_unit.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
product_promo_code_association_table = sa.Table(
    "product_promo_code_association",
    Base.metadata,
    sa.Column(
        "product_media_id",
        sa.ForeignKey("product_promo_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
product_category_association_table = sa.Table(
    "product_category_association",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "category_id",
        sa.ForeignKey("product_category.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
