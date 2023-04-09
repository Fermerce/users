from lib.db.primary_key import Base, sa


product_media_table = sa.Table(
    "product_media_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "media_id",
        sa.ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
product_promo_codes_table = sa.Table(
    "product_promo_code_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "promo_code_id",
        sa.ForeignKey("product_promo_code.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
product_category_association_table = sa.Table(
    "product_category_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "product_category_id",
        sa.ForeignKey("product_category.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
product_measuring_unit_association_table = sa.Table(
    "product_measuring_unit_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "product_measuring_unit_id",
        sa.ForeignKey("product_measuring_unit.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

product_state_association_table = sa.Table(
    "product_avail_state_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "state_id",
        sa.ForeignKey("state.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

product_country_association_table = sa.Table(
    "product_avail_country_ass",
    Base.metadata,
    sa.Column(
        "product_id",
        sa.ForeignKey("product.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "country_id",
        sa.ForeignKey("country.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
