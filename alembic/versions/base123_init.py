"""Initial empty script for alembic.

Revision ID: base123
Revises: 
Create Date: 2024-05-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'base123'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
