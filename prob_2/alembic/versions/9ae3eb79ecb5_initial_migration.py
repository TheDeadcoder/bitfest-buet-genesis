"""Initial migration

Revision ID: 9ae3eb79ecb5
Revises: 66fa48cb7d42
Create Date: 2024-12-21 19:20:00.188977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ae3eb79ecb5'
down_revision: Union[str, None] = '66fa48cb7d42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###