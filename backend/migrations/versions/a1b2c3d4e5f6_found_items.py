"""create found_items table if not exists

Revision ID: a1b2c3d4e5f6
Revises: 6488c234c9ec
Create Date: 2025-11-14 23:30:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "6488c234c9ec"
branch_labels = None
depends_on = None


def upgrade():
    # -----------------------------
    # Create found_items table
    # -----------------------------
    conn = op.get_bind()
    inspector = inspect(conn)
    if "found_items" not in inspector.get_table_names():
        op.create_table(
            "found_items",
            sa.Column(
                "id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
            ),
            sa.Column("lat", sa.Float(), nullable=False),
            sa.Column("lon", sa.Float(), nullable=False),
            sa.Column(
                "type_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("item_type.id"),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.func.now(),
            ),
        )


def downgrade():
    op.drop_table("found_items")
