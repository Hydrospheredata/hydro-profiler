"""add_column_to_aggregation

Revision ID: b99136c7fa84
Revises: d5396aab1e55
Create Date: 2021-12-15 21:15:51.642876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b99136c7fa84"
down_revision = "d5396aab1e55"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "aggregations",
        sa.Column("batch_rows_count", sa.Integer(), nullable=False, default=0),
    )


def downgrade():
    op.drop_column("aggregations", "batch_rows_count")
