"""Adding field
Revision ID: 3d151be968c0
Revises: 570e3f4e6024
Create Date: 2022-05-11 15:56:01.710604
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '3d151be968c0'
down_revision = '570e3f4e6024'
branch_labels = None
depends_on = None
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quantity_code', sa.Column('abbreviation', sa.String(length=16), nullable=True))
    op.create_index(op.f('ix_quantity_code_abbreviation'), 'quantity_code', ['abbreviation'], unique=False)
    # ### end Alembic commands ###
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_quantity_code_abbreviation'), table_name='quantity_code')
    op.drop_column('quantity_code', 'abbreviation')
    # ### end Alembic commands ###