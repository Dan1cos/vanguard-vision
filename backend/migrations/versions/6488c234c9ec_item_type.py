"""create item_type table

Revision ID: 6488c234c9ec
Revises:
Create Date: 2025-11-14 23:05:33.216802

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6488c234c9ec"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -----------------------------
    # Create item_type table
    # -----------------------------
    op.create_table(
        "item_type",
        sa.Column(
            "id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("explosion_radius", sa.Float(), nullable=False),
    )


def downgrade():
    op.drop_table("item_type")
