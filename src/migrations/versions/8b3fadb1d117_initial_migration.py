"""initial migration

Revision ID: 8b3fadb1d117
Revises: 
Create Date: 2026-07-15 18:40:14.532090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '8b3fadb1d117'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('books')

