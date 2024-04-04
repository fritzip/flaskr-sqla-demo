"""tag name unique

Revision ID: 81b2a74aec53
Revises: c44201f272ff
Create Date: 2024-04-04 18:20:11.758713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81b2a74aec53'
down_revision = 'c44201f272ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_tag_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_tag_name'), type_='unique')

    # ### end Alembic commands ###