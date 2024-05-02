"""add a role column

Revision ID: 1d35b92908e7
Revises: 69e034411b09
Create Date: 2024-05-02 12:05:57.547045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d35b92908e7'
down_revision: Union[str, None] = '69e034411b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('roles', sa.ARRAY(sa.String()), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'roles')
    # ### end Alembic commands ###
