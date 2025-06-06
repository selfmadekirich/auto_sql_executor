"""New Migration

Revision ID: 2d99d079c3f8
Revises: 
Create Date: 2024-12-16 23:51:38.238650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d99d079c3f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_connections',
    sa.Column('db_type', sa.String(), nullable=False),
    sa.Column('json_props', sa.JSON(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_db_connections_id'), 'db_connections', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_db_connections_id'), table_name='db_connections')
    op.drop_table('db_connections')
    # ### end Alembic commands ###
