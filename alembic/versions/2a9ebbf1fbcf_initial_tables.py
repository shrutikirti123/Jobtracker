"""initial tables

Revision ID: 2a9ebbf1fbcf
Revises: 
Create Date: 2026-03-08 15:03:11.945193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a9ebbf1fbcf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String()),
        sa.Column('role', sa.String()),
        sa.Column('email', sa.String(), unique=True),
        sa.Column('password', sa.String()),
        sa.Column('skills', sa.String())
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String()),
        sa.Column('company', sa.String()),
        sa.Column('status', sa.String()),
        sa.Column('description', sa.String()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'))
    )

def downgrade():

    op.drop_table('jobs')
    op.drop_table('users')