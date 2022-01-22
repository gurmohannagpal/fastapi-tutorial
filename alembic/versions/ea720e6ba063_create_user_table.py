"""create_user table

Revision ID: ea720e6ba063
Revises: b618dcc94a40
Create Date: 2022-01-21 16:39:25.107011

"""
from sqlite3 import Timestamp
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea720e6ba063'
down_revision = 'b618dcc94a40'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
