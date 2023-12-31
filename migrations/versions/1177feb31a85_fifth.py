"""'Fifth'

Revision ID: 1177feb31a85
Revises: c74247965951
Create Date: 2023-12-01 21:58:02.809940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1177feb31a85'
down_revision: Union[str, None] = 'c74247965951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('lastname', sa.String(length=50), nullable=True))
    op.drop_column('contacts', 'secondname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('secondname', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('contacts', 'lastname')
    # ### end Alembic commands ###
