"""add foreign-key to posts table

Revision ID: 3c5652ef45d1
Revises: 578ad2bd0135
Create Date: 2022-01-22 00:25:07.907505

"""
from tkinter import CASCADE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c5652ef45d1'
down_revision = '578ad2bd0135'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
