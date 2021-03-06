"""empty message

Revision ID: 203f7b2e3c72
Revises: 0fc023b77de6
Create Date: 2017-10-12 18:10:57.622430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203f7b2e3c72'
down_revision = '0fc023b77de6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
