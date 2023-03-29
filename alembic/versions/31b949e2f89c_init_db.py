"""init db

Revision ID: 31b949e2f89c
Revises: 
Create Date: 2023-03-29 02:05:53.603261

"""
from alembic import op
import sqlalchemy as sa
import src

# revision identifiers, used by Alembic.
revision = '31b949e2f89c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_token',
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('ip_address', sa.String(length=24), nullable=True),
    sa.Column('id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer',
    sa.Column('firstname', sa.String(length=20), nullable=True),
    sa.Column('lastname', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('password_reset_token', sa.String(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_suspended', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('permission',
    sa.Column('name', sa.String(length=24), nullable=True),
    sa.Column('id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff',
    sa.Column('aud', sa.String(length=8), nullable=True),
    sa.Column('firstname', sa.String(length=20), nullable=True),
    sa.Column('lastname', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_suspended', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('password_reset_token', sa.String(), nullable=True),
    sa.Column('tel', sa.String(length=17), nullable=True),
    sa.Column('id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('customer_role_association',
    sa.Column('customer_id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('permission_id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.PrimaryKeyConstraint('customer_id', 'permission_id')
    )
    op.create_table('staff_role_association',
    sa.Column('staff_id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.Column('permission_id', src.lib.db.primary_key.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.PrimaryKeyConstraint('staff_id', 'permission_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('staff_role_association')
    op.drop_table('customer_role_association')
    op.drop_table('staff')
    op.drop_table('permission')
    op.drop_table('customer')
    op.drop_table('auth_token')
    # ### end Alembic commands ###
