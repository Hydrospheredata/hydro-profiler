"""initial

Revision ID: fe734aec08dc
Revises: 
Create Date: 2021-12-08 21:48:39.394217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fe734aec08dc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "metrics",
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("model_version", sa.Integer(), nullable=False),
        sa.Column("metrics", sa.Text()),
    )

    op.create_table(
        "reports",
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("model_version", sa.Integer(), nullable=False),
        sa.Column("batch_name", sa.String(), nullable=False),
        sa.Column("file_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("report", sa.Text(), nullable=False),
    )

    op.create_table(
        "aggregations",
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("model_version", sa.Integer(), nullable=False),
        sa.Column("batch_name", sa.String(), nullable=False),
        sa.Column("file_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("aggregation", sa.Text(), nullable=False),
    )

    op.create_table(
        "overall_reports",
        sa.Column("model_name", sa.String(), nullable=False),
        sa.Column("model_version", sa.Integer(), nullable=False),
        sa.Column("batch_name", sa.String(), nullable=False),
        sa.Column("suspicious_percent", sa.Float(), nullable=False),
        sa.Column("failed_ratio", sa.Float(), nullable=False),
    )


def downgrade():
    op.drop_table("metrics")
    op.drop_table("reports")
    op.drop_table("aggregations")
    op.drop_table("overall_reports")
