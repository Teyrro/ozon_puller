"""create table users

Revision ID: c56372749340
Revises:
Create Date: 2024-04-22 18:04:21.440813

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c56372749340"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("surname", sa.String(length=30), nullable=False),
        sa.Column("email", sa.String(length=40), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
