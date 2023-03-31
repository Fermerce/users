"""add username to customer

Revision ID: a0fc7033fed6
Revises: cc3b9385229f
Create Date: 2023-03-29 17:00:11.027857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0fc7033fed6"
down_revision = "cc3b9385229f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("customer", sa.Column("username", sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("customer", "username")
    # ### end Alembic commands ###