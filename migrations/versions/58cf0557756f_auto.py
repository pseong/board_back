"""Auto

Revision ID: 58cf0557756f
Revises: 3ee8518a38e0
Create Date: 2022-08-25 14:43:29.935580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58cf0557756f'
down_revision = '3ee8518a38e0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_tbl', sa.Column('created_date', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('board_tbl', 'created_date')
    # ### end Alembic commands ###
