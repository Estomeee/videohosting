"""Creation table video

Revision ID: 96af8a8e14b9
Revises: d565a206af62
Create Date: 2023-06-04 17:04:26.545947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96af8a8e14b9'
down_revision = 'd565a206af62'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=60), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('count_likes', sa.Integer(), nullable=True),
                    sa.Column('id_auther', sa.Integer(), nullable=False),
                    sa.Column('video_link', sa.String(), nullable=False),
                    sa.Column('poster_link', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['id_auther'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    # ### end Alembic commands ###
