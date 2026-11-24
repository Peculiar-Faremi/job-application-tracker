"""rename applications table

Revision ID: 994c93265946
Revises: 7679a4b5fa57
Create Date: 2026-11-24 11:23:21.518303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '994c93265946'
down_revision: Union[str, Sequence[str], None] = '7679a4b5fa57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
