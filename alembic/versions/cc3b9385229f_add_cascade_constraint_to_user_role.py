"""add cascade constraint to user role

Revision ID: cc3b9385229f
Revises: 31b949e2f89c
Create Date: 2023-03-29 02:17:52.040937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc3b9385229f'
down_revision = '31b949e2f89c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('customer_role_association_customer_id_fkey', 'customer_role_association', type_='foreignkey')
    op.drop_constraint('customer_role_association_permission_id_fkey', 'customer_role_association', type_='foreignkey')
    op.create_foreign_key(None, 'customer_role_association', 'customer', ['customer_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'customer_role_association', 'permission', ['permission_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint('staff_role_association_permission_id_fkey', 'staff_role_association', type_='foreignkey')
    op.drop_constraint('staff_role_association_staff_id_fkey', 'staff_role_association', type_='foreignkey')
    op.create_foreign_key(None, 'staff_role_association', 'permission', ['permission_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.create_foreign_key(None, 'staff_role_association', 'staff', ['staff_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff_role_association', type_='foreignkey')
    op.drop_constraint(None, 'staff_role_association', type_='foreignkey')
    op.create_foreign_key('staff_role_association_staff_id_fkey', 'staff_role_association', 'staff', ['staff_id'], ['id'])
    op.create_foreign_key('staff_role_association_permission_id_fkey', 'staff_role_association', 'permission', ['permission_id'], ['id'])
    op.drop_constraint(None, 'customer_role_association', type_='foreignkey')
    op.drop_constraint(None, 'customer_role_association', type_='foreignkey')
    op.create_foreign_key('customer_role_association_permission_id_fkey', 'customer_role_association', 'permission', ['permission_id'], ['id'])
    op.create_foreign_key('customer_role_association_customer_id_fkey', 'customer_role_association', 'customer', ['customer_id'], ['id'])
    # ### end Alembic commands ###