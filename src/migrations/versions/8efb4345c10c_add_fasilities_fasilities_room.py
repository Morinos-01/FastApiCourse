"""add fasilities, fasilities_room

Revision ID: 8efb4345c10c
Revises: 0e71251cb7e4
Create Date: 2026-09-07 15:44:48.803527

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8efb4345c10c"
down_revision: Union[str, Sequence[str], None] = "0e71251cb7e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "fasilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_fasilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("fasilitie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["fasilitie_id"],
            ["fasilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("rooms_fasilities")
    op.drop_table("fasilities")
