from utils.general import get_date
from app import db

product_category_association = db.Table(
    "product_category_association",
    db.Model.metadata,
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("product_category.id")),
)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    sub_title = db.Column(db.String(500), nullable=True)
    properties = db.Column(db.Text)
    description = db.Column(db.Text)
    price = db.Column(db.Double(2))
    stocks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=get_date)
    updated_at = db.Column(db.DateTime, default=get_date, onupdate=get_date)

    # Relations
    product_id = db.relationship("ProductPicture", backref="product")
    categories = db.relationship(
        "ProductCategory",
        secondary=product_category_association,
        back_populates="products",
    )


class ProductPicture(db.Model):
    __tablename__ = "product_picture"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.Text, nullable=False)

    # Relations
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))


class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship(
        "Product",
        secondary=product_category_association,
        back_populates="categories",
    )
