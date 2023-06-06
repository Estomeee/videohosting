"""Remove like, sub for recreate

Revision ID: 01ca4434040e
Revises: f585f8b16603
Create Date: 2023-06-06 15:08:42.776982

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '01ca4434040e'
down_revision = 'f585f8b16603'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sub')
    op.drop_table('like')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id_video', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_auther', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('published_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_auther'], ['user.id'], name='like_id_auther_fkey'),
    sa.ForeignKeyConstraint(['id_video'], ['video.id'], name='like_id_video_fkey')
    )
    op.create_table('sub',
    sa.Column('id_maker', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_subscriber', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_maker'], ['user.id'], name='sub_id_maker_fkey'),
    sa.ForeignKeyConstraint(['id_subscriber'], ['user.id'], name='sub_id_subscriber_fkey')
    )
    # ### end Alembic commands ###