"""Alter column in folder_id

Revision ID: 2cff31de7393
Revises: 3fdede2ff32c
Create Date: 2023-11-04 13:45:37.105580
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2cff31de7393'
down_revision = '3fdede2ff32c'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.alter_column('folder_id', existing_type=sa.INTEGER(), nullable=True)

def downgrade():
    with op.batch_alter_table('files', schema=None) as batch_op:
        batch_op.alter_column('folder_id', existing_type=sa.INTEGER(), nullable=False)

