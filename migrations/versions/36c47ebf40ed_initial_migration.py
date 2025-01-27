"""Initial migration

Revision ID: 36c47ebf40ed
Revises: 
Create Date: 2025-01-15 15:12:12.266001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36c47ebf40ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('sub_title', sa.String(length=500), nullable=True),
    sa.Column('properties', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Double(precision=2), nullable=True),
    sa.Column('stocks', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('product_picture',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('braintree_transaction_id', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('customer_email', sa.String(length=250), nullable=False),
    sa.Column('customer_name', sa.String(length=250), nullable=True),
    sa.Column('invoice_number', sa.String(length=50), nullable=False),
    sa.Column('billing_address', sa.Text(), nullable=True),
    sa.Column('shipping_address', sa.Text(), nullable=True),
    sa.Column('issued_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('braintree_transaction_id'),
    sa.UniqueConstraint('invoice_number')
    )
    op.create_table('user_cart',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=75), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('phone_number', sa.String(length=21), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('profile_picture', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart_product',
    sa.Column('user_cart_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_cart_id'], ['user_cart.id'], )
    )
    op.create_table('transaction_product',
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_product')
    op.drop_table('cart_product')
    op.drop_table('user_profile')
    op.drop_table('user_cart')
    op.drop_table('transaction')
    op.drop_table('product_picture')
    op.drop_table('user')
    op.drop_table('product')
    # ### end Alembic commands ###
