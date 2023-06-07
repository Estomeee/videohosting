"""Integer to BigInteger

Revision ID: 8b96feb02903
Revises: 703b41e52179
Create Date: 2023-06-07 23:36:42.156846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b96feb02903'
down_revision = '703b41e52179'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('video', 'id', type_=sa.BigInteger, postgresql_using='id::bigint')
    op.alter_column('comment', 'id', type_=sa.BigInteger, postgresql_using='id::bigint')
    op.alter_column('comment', 'id_video', type_=sa.BigInteger, postgresql_using='id_video::bigint')
    op.alter_column('like', 'id_video', type_=sa.BigInteger, postgresql_using='id_video::bigint')
    op.alter_column('view', 'id_video', type_=sa.BigInteger, postgresql_using='id_video::bigint')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
