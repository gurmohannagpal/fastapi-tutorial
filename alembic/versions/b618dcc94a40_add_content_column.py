"""Add content column

Revision ID: b618dcc94a40
Revises: bf63a2fae325
Create Date: 2022-01-21 16:26:34.029578

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b618dcc94a40'
down_revision = 'bf63a2fae325'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
