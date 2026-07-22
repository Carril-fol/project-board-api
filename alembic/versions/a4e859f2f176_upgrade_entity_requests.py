"""upgrade entity requests

Revision ID: a4e859f2f176
Revises: 4fb5e863b32b
Create Date: 2026-07-22 00:16:54.001482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4e859f2f176'
down_revision: Union[str, Sequence[str], None] = '4fb5e863b32b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
