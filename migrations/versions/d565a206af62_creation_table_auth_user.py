"""Creation table auth_user

Revision ID: d565a206af62
Revises: f26bb0ad6701
Create Date: 2023-06-04 12:57:52.010164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd565a206af62'
down_revision = 'f26bb0ad6701'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=30), nullable=True),
                    sa.Column('fullname', sa.String(), nullable=True),
                    sa.Column('email', sa.String(length=320), nullable=False),
                    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('is_verified', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###