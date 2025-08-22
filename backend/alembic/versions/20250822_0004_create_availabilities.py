from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20250822_0004"
down_revision = "20250822_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "availabilities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("intermittent_id", sa.Integer(), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=False), nullable=False),
        sa.Column("busy", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("note", sa.String(length=200), nullable=True),
    )
    op.create_index("ix_avail_inter_id", "availabilities", ["intermittent_id"])
    op.create_index("ix_avail_time", "availabilities", ["start_at", "end_at"])


def downgrade() -> None:
    op.drop_index("ix_avail_time", table_name="availabilities")
    op.drop_index("ix_avail_inter_id", table_name="availabilities")
    op.drop_table("availabilities")
