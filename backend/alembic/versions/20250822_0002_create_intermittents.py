from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20250822_0002"
down_revision = "20250822_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "intermittents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")
        ),
        sa.Column("skills", sa.String(length=200), nullable=True),
    )
    op.create_unique_constraint(
        "uq_intermittents_name",
        "intermittents",
        ["first_name", "last_name"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_intermittents_name", "intermittents", type_="unique"
    )
    op.drop_table("intermittents")
