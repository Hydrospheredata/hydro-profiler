"""create models table

Revision ID: d5396aab1e55
Revises: fe734aec08dc
Create Date: 2021-12-15 18:22:55.762080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d5396aab1e55"
down_revision = "fe734aec08dc"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "models",
        sa.Column(
            "model_name",
            sa.String(),
            nullable=False,
        ),
        sa.Column("model_version", sa.Integer(), nullable=False),
        sa.Column("contract", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table("models")
