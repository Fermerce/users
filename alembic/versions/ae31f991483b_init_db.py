"""init db

Revision ID: ae31f991483b
Revises: 
Create Date: 2023-04-06 19:08:47.125338

"""
from alembic import op
import ormar
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ae31f991483b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_token",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("refresh_token", sa.String(length=255), nullable=True),
        sa.Column("access_token", sa.String(length=255), nullable=True),
        sa.Column("aud", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("ip_address", sa.String(length=24), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("firstname", sa.String(length=20), nullable=True),
        sa.Column("lastname", sa.String(length=20), nullable=True),
        sa.Column("username", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=300), nullable=False),
        sa.Column("password_reset_token", sa.String(length=300), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_suspended", sa.Boolean(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "p_category",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "p_promocode",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("code", sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "permission",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_detail",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("detail", sa.String(length=5000), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_measuring_unit",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("unit", sa.String(length=24), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "media",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("alt", sa.String(length=225), nullable=False),
        sa.Column("url", sa.String(length=225), nullable=False),
        sa.Column("content_type", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("aud", sa.String(length=10), nullable=True),
        sa.Column("firstname", sa.String(length=20), nullable=True),
        sa.Column("lastname", sa.String(length=20), nullable=True),
        sa.Column("username", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=300), nullable=False),
        sa.Column("password_reset_token", sa.String(length=300), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_suspended", sa.Boolean(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("tel", sa.String(length=17), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "users_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("permission", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.Column("user", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["user"],
            ["users.id"],
            name="fk_user_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["permission"],
            ["permission.id"],
            name="fk_permission_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product",
        sa.Column("id", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("slug", sa.String(length=300), nullable=False),
        sa.Column("stock_unit", sa.Integer(), nullable=True),
        sa.Column("original_price", sa.Float(), nullable=True),
        sa.Column("sale_price", sa.Float(), nullable=False),
        sa.Column("discount", sa.Float(), nullable=True),
        sa.Column("sku", sa.String(length=16), nullable=True),
        sa.Column("description", sa.String(length=5000), nullable=False),
        sa.Column("is_series", sa.Boolean(), nullable=True),
        sa.Column("in_stock", sa.Boolean(), nullable=True),
        sa.Column("is_suspended", sa.Boolean(), nullable=True),
        sa.Column("details", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.Column("medias", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["details"], ["product_detail.id"], name="fk_product_details"
        ),
        sa.ForeignKeyConstraint(["medias"], ["media.id"], name="fk_medias"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staffs_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("permission", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.Column("staff", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission"],
            ["permission.id"],
            name="fk_permission_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["staff"],
            ["staff.id"],
            name="fk_staff_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "products_productcategorys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "productcategory", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True
        ),
        sa.Column("product", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["product"],
            ["product.id"],
            name="fk_products_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["productcategory"],
            ["p_category.id"],
            name="fk_products_category_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "products_productmeasuringunits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "productmeasuringunit", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True
        ),
        sa.Column("product", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["product"],
            ["product.id"],
            name="fk_products_munit_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["productmeasuringunit"],
            ["product_measuring_unit.id"],
            name="fk_meunit__id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "products_productpromocodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "productpromocode", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True
        ),
        sa.Column("product", ormar.fields.sqlalchemy_uuid.CHAR(36), nullable=True),
        sa.ForeignKeyConstraint(
            ["product"],
            ["product.id"],
            name="fk_products_productpromocodes_product_product_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["productpromocode"],
            ["p_promocode.id"],
            name="fk_products_productpromocode_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("products_productpromocodes")
    op.drop_table("products_productmeasuringunits")
    op.drop_table("products_productcategorys")
    op.drop_table("staffs_permissions")
    op.drop_table("product")
    op.drop_table("users_permissions")
    op.drop_table("staff")
    op.drop_table("media")
    op.drop_table("product_measuring_unit")
    op.drop_table("product_detail")
    op.drop_table("permission")
    op.drop_table("p_promocode")
    op.drop_table("p_category")
    op.drop_table("users")
    op.drop_table("auth_token")
    # ### end Alembic commands ###
