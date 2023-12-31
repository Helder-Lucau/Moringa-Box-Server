"""created users,files and folder tables

Revision ID: 3fdede2ff32c
Revises: 39f83367c379
Create Date: 2023-10-26 12:10:12.915850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fdede2ff32c'
down_revision = '39f83367c379'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('folders',
    sa.Column('folder_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('folder_name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('parent_folder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('folder_id')
    )
    op.create_table('files',
    sa.Column('file_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('file_path', sa.String(length=255), nullable=False),
    sa.Column('file_image', sa.String(length=255), nullable=True),
    sa.Column('file_type', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('folder_id', sa.Integer(), nullable=False),
    sa.Column('upload_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['folder_id'], ['folders.folder_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('file_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('files')
    op.drop_table('folders')
    op.drop_table('users')
    # ### end Alembic commands ###
