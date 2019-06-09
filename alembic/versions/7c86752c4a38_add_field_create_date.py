"""add_field_create_date

Revision ID: 7c86752c4a38
Revises: 2e8e603859e2
Create Date: 2019-06-09 21:07:17.573918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c86752c4a38'
down_revision = '2e8e603859e2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('student', sa.Column('create_date', sa.Date(), nullable=True))


def downgrade():
    with op.batch_alter_table('student') as batch_op:
        batch_op.drop_column('create_date')
