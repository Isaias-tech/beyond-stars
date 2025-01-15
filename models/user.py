from utils.general import get_date
from flask_login import UserMixin
from app import db

cart_product = db.Table(
    "cart_product",
    db.Column("user_cart_id", db.Integer, db.ForeignKey("user_cart.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("quantity", db.Integer),
)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_date)
    updated_at = db.Column(db.DateTime, default=get_date, onupdate=get_date)

    # Relations
    user_profile = db.relationship("UserProfile", backref="user", uselist=False)
    user_cart = db.relationship("UserCart", backref="user", uselist=False)
    transaction = db.relationship("Transaction", backref="user")


class UserProfile(db.Model):
    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(21), nullable=True)
    address = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.Text, default="/default_pictures/user_profile.svg")

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class UserCart(db.Model):
    __tablename__ = "user_cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    products = db.relationship("Product", secondary=cart_product, backref="user_cart")
