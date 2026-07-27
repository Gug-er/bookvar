"""refactor email in users now unique

Revision ID: 2a98688d1a51
Revises: 8b3fadb1d117
Create Date: 2026-07-27 18:43:46.116587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2a98688d1a51'
down_revision: Union[str, Sequence[str], None] = '8b3fadb1d117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('super_user', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('books', sa.Column('annotation', sa.String(), nullable=False))
    op.add_column('books', sa.Column('genre', sa.String(), nullable=False))
    op.drop_column('books', 'description')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('books', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('books', 'genre')
    op.drop_column('books', 'annotation')
    op.drop_table('users')
