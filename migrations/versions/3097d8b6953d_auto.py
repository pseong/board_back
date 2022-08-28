"""Auto

Revision ID: 3097d8b6953d
Revises: 
Create Date: 2022-08-25 14:18:43.262488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3097d8b6953d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tbl',
    sa.Column('user_rid', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('user_rid')
    )
    op.create_index(op.f('ix_user_tbl_id'), 'user_tbl', ['id'], unique=False)
    op.create_index(op.f('ix_user_tbl_password'), 'user_tbl', ['password'], unique=True)
    op.create_index(op.f('ix_user_tbl_user_rid'), 'user_tbl', ['user_rid'], unique=False)
    op.create_table('board_tbl',
    sa.Column('board_rid', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=True),
    sa.Column('user_rid', sa.Integer(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_rid'], ['user_tbl.user_rid'], ),
    sa.PrimaryKeyConstraint('board_rid')
    )
    op.create_index(op.f('ix_board_tbl_board_rid'), 'board_tbl', ['board_rid'], unique=False)
    op.create_index(op.f('ix_board_tbl_subject'), 'board_tbl', ['subject'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_board_tbl_subject'), table_name='board_tbl')
    op.drop_index(op.f('ix_board_tbl_board_rid'), table_name='board_tbl')
    op.drop_table('board_tbl')
    op.drop_index(op.f('ix_user_tbl_user_rid'), table_name='user_tbl')
    op.drop_index(op.f('ix_user_tbl_password'), table_name='user_tbl')
    op.drop_index(op.f('ix_user_tbl_id'), table_name='user_tbl')
    op.drop_table('user_tbl')
    # ### end Alembic commands ###
