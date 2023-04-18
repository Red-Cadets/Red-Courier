"""auto

Revision ID: 1c73cb159744
Revises: b097d1e0cf99
Create Date: 2023-04-17 22:27:23.822047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c73cb159744'
down_revision = 'b097d1e0cf99'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('mention', sa.String(length=255), nullable=True),
    sa.Column('link', sa.String(length=225), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_table('chats')
    # ### end Alembic commands ###
