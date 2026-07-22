"""upgrade entity requests

Revision ID: 2faba67fbda0
Revises: a4e859f2f176
Create Date: 2026-07-22 00:27:29.946856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2faba67fbda0'
down_revision: Union[str, Sequence[str], None] = 'a4e859f2f176'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
