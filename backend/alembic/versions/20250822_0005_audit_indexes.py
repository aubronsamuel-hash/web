from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "20250822_0005"
down_revision = "20250822_0004"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index("ix_audit_request_id", "audit_logs", ["request_id"])
    op.create_index("ix_audit_ts", "audit_logs", ["ts"])
    op.create_index("ix_audit_entity", "audit_logs", ["entity"])
    op.create_index("ix_audit_action", "audit_logs", ["action"])

def downgrade() -> None:
    op.drop_index("ix_audit_action", table_name="audit_logs")
    op.drop_index("ix_audit_entity", table_name="audit_logs")
    op.drop_index("ix_audit_ts", table_name="audit_logs")
    op.drop_index("ix_audit_request_id", table_name="audit_logs")
