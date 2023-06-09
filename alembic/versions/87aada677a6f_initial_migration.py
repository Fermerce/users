"""initial migration

Revision ID: 87aada677a6f
Revises: 
Create Date: 2023-04-07 01:32:31.228065

"""
from alembic import op
import sqlalchemy as sa
import lib

# revision identifiers, used by Alembic.
revision = "87aada677a6f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_token",
        sa.Column("refresh_token", sa.String(), nullable=True),
        sa.Column("access_token", sa.String(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("ip_address", sa.String(length=24), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("firstname", sa.String(length=20), nullable=True),
        sa.Column("lastname", sa.String(length=20), nullable=True),
        sa.Column("username", sa.String(length=30), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("password_reset_token", sa.String(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_suspended", sa.Boolean(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "permission",
        sa.Column("name", sa.String(length=24), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_category",
        sa.Column("name", sa.String(length=24), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_measuring_unit",
        sa.Column("unit", sa.String(length=24), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product_promo_code",
        sa.Column("code", sa.String(length=10), nullable=True),
        sa.Column("discount", sa.Float(), nullable=False),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "country",
        sa.Column("name", sa.String(length=24), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff",
        sa.Column("aud", sa.String(length=8), nullable=True),
        sa.Column("firstname", sa.String(length=20), nullable=True),
        sa.Column("lastname", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_suspended", sa.Boolean(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("password_reset_token", sa.String(), nullable=True),
        sa.Column("tel", sa.String(length=17), nullable=True),
        sa.Column("id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "users_role_association",
        sa.Column("users_id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("permission_id", lib.db.primary_key.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["users_id"], [" user.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"], ["permission.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("users_id", "permission_id"),
    )
    op.create_table(
        "staff_role_association",
        sa.Column("staff_id", lib.db.primary_key.GUID(), nullable=False),
        sa.Column("permission_id", lib.db.primary_key.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["permission_id"], ["permission.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["staff_id"], ["staff.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("staff_id", "permission_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("staff_role_association")
    op.drop_table("users_role_association")
    op.drop_table("staff")
    op.drop_table("country")
    op.drop_table("product_promo_code")
    op.drop_table("product_measuring_unit")
    op.drop_table("product_category")
    op.drop_table("permission")
    op.drop_table("user")
    op.drop_table("auth_token")
    # ### end Alembic commands ###
