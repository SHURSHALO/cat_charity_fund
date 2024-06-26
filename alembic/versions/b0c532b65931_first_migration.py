"""First migration

Revision ID: b0c532b65931
Revises: 
Create Date: 2024-03-20 18:41:14.250392

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0c532b65931'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'charityproject',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=True),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=True),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    op.drop_table('charityproject')
    # ### end Alembic commands ###
