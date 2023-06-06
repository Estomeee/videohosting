"""Add attr datatime2

Revision ID: 02bc0007d102
Revises: 60c61582f584
Create Date: 2023-06-06 17:08:34.957653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02bc0007d102'
down_revision = '60c61582f584'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('like', sa.Column('published_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('like', 'published_at')
    # ### end Alembic commands ###
