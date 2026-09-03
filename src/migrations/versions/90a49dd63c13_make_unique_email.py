"""make unique email

Revision ID: 90a49dd63c13
Revises: a706e4806d21
Create Date: 2026-09-03 15:51:46.399454

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "90a49dd63c13"
down_revision: Union[str, Sequence[str], None] = "a706e4806d21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
