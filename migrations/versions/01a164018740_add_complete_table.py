"""add complete table

Revision ID: 01a164018740
Revises: c1b00ba07f6d
Create Date: 2020-10-30 11:36:42.870814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01a164018740'
down_revision = 'c1b00ba07f6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolists', 'complete')
    # ### end Alembic commands ###