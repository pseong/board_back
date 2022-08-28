"""Auto

Revision ID: c3e23b08716e
Revises: ddf1118a07bd
Create Date: 2022-08-25 14:26:15.491792

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3e23b08716e'
down_revision = 'ddf1118a07bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_tbl', sa.Column('parent_rid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'board_tbl', 'board_tbl', ['parent_rid'], ['board_rid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'board_tbl', type_='foreignkey')
    op.drop_column('board_tbl', 'parent_rid')
    # ### end Alembic commands ###