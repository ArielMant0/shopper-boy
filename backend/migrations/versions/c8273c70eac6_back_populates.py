"""back populates

Revision ID: c8273c70eac6
Revises: f1d74a17eed0
Create Date: 2023-05-21 18:17:01.053331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8273c70eac6'
down_revision = 'f1d74a17eed0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand_products', schema=None) as batch_op:
        batch_op.drop_constraint('unique_name_product', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_brand_products_name'), ['name', 'product_id'])

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('unique_name_category', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_products_name'), ['name', 'category_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_products_name'), type_='unique')
        batch_op.create_unique_constraint('unique_name_category', ['name', 'category_id'])

    with op.batch_alter_table('brand_products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_brand_products_name'), type_='unique')
        batch_op.create_unique_constraint('unique_name_product', ['name', 'product_id'])

    # ### end Alembic commands ###
