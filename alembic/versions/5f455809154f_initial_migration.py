"""Initial migration

Revision ID: 5f455809154f
Revises: 
Create Date: 2024-07-24 15:12:56.495275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f455809154f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bloodborne_characters',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('origin', sa.String(), nullable=True),
    sa.Column('weapon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_index(op.f('ix_bloodborne_characters_name'), 'bloodborne_characters', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bloodborne_characters_name'), table_name='bloodborne_characters')
    op.drop_table('bloodborne_characters')
    # ### end Alembic commands ###
