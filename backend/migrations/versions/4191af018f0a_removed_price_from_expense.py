"""removed price from expense

Revision ID: 4191af018f0a
Revises: 929c607db92b
Create Date: 2023-05-08 22:01:01.278928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4191af018f0a'
down_revision = '929c607db92b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brand_products', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_brand_products_name'), ['name'])

    with op.batch_alter_table('daily_meal_plans', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_daily_meal_plans_date'), ['date'])

    with op.batch_alter_table('product_categories', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_product_categories_name'), ['name'])

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_products_name'), ['name'])

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.drop_column('price')

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_recipes_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_recipes_name'), type_='unique')

    with op.batch_alter_table('receipts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.FLOAT(), nullable=False))

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_products_name'), type_='unique')

    with op.batch_alter_table('product_categories', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_product_categories_name'), type_='unique')

    with op.batch_alter_table('daily_meal_plans', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_daily_meal_plans_date'), type_='unique')

    with op.batch_alter_table('brand_products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_brand_products_name'), type_='unique')

    # ### end Alembic commands ###