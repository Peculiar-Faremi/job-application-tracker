"""rename applications table

Revision ID: 7679a4b5fa57
Revises: c87af78f4b08
Create Date: 2026-11-24 11:02:43.156681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7679a4b5fa57'
down_revision: Union[str, Sequence[str], None] = 'c87af78f4b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("Applications", "applications")
    pass


def downgrade() -> None:
    op.rename_table("applications", "Applications")
    pass
