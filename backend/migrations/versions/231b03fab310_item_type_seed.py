"""item_type seed data

Revision ID: 231b03fab310
Revises: a1b2c3d4e5f6
Create Date: 2025-11-14 23:14:53.030959

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "231b03fab310"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # -----------------------------
    # Seed item_type
    # -----------------------------
    op.bulk_insert(
        sa.table(
            "item_type",
            sa.Column("id", postgresql.UUID(as_uuid=True)),
            sa.Column("title", sa.String),
            sa.Column("explosion_radius", sa.Float),
        ),
        [
            {
                "id": str(uuid.uuid4()),
                "title": "aircraft-bombs",
                "explosion_radius": 100,
            },
            {"id": str(uuid.uuid4()), "title": "fuzes", "explosion_radius": 5},
            {"id": str(uuid.uuid4()), "title": "grenades", "explosion_radius": 10},
            {"id": str(uuid.uuid4()), "title": "landmines", "explosion_radius": 8},
            {"id": str(uuid.uuid4()), "title": "mortars", "explosion_radius": 20},
            {"id": str(uuid.uuid4()), "title": "projectiles", "explosion_radius": 30},
            {"id": str(uuid.uuid4()), "title": "rockets", "explosion_radius": 40},
            {"id": str(uuid.uuid4()), "title": "submunitions", "explosion_radius": 6},
        ],
    )


def downgrade() -> None:
    # Remove only the rows that were inserted by this seed migration
    op.execute(
        """
        DELETE FROM item_type
        WHERE title IN (
            'aircraft-bombs', 'fuzes', 'grenades', 'landmines',
            'mortars', 'projectiles', 'rockets', 'submunitions'
        );
    """
    )
