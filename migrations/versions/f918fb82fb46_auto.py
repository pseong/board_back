"""Auto

Revision ID: f918fb82fb46
Revises: 58cf0557756f
Create Date: 2022-08-25 18:10:49.042017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f918fb82fb46'
down_revision = '58cf0557756f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_tbl', sa.Column('content', sa.Text(), nullable=False))
    op.alter_column('board_tbl', 'subject',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('board_tbl', 'created_date',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.drop_index('ix_user_tbl_id', table_name='user_tbl')
    op.create_index(op.f('ix_user_tbl_id'), 'user_tbl', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_tbl_id'), table_name='user_tbl')
    op.create_index('ix_user_tbl_id', 'user_tbl', ['id'], unique=False)
    op.alter_column('board_tbl', 'created_date',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('board_tbl', 'subject',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.drop_column('board_tbl', 'content')
    # ### end Alembic commands ###
