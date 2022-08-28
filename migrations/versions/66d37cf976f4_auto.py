"""Auto

Revision ID: 66d37cf976f4
Revises: 3097d8b6953d
Create Date: 2022-08-25 14:20:54.025085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66d37cf976f4'
down_revision = '3097d8b6953d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_tbl', sa.Column('nickname', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_tbl', 'nickname')
    # ### end Alembic commands ###