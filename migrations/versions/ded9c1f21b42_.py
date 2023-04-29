"""empty message

Revision ID: ded9c1f21b42
Revises: f8cb55412aa5
Create Date: 2023-04-29 17:17:05.739149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded9c1f21b42'
down_revision = 'f8cb55412aa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_image', sa.String(length=80), nullable=True))
        batch_op.create_unique_constraint(None, ['user_image'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_image')

    # ### end Alembic commands ###