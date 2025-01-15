from utils.general import get_date
from sqlalchemy import func
from app import db

transaction_product = db.Table(
    "transaction_product",
    db.Column("transaction_id", db.Integer, db.ForeignKey("transaction.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("quantity", db.Integer),
)


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    braintree_transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="USD")
    payment_method = db.Column(db.String(50), nullable=False)
    customer_email = db.Column(db.String(250), nullable=False)
    customer_name = db.Column(db.String(250), nullable=True)

    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    billing_address = db.Column(db.Text, nullable=True)
    shipping_address = db.Column(db.Text, nullable=True)
    issued_at = db.Column(db.DateTime, default=get_date)

    # Relations
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    products = db.relationship(
        "Product",
        secondary=transaction_product,
        backref="transactions",
    )

    @staticmethod
    def generate_invoice_number():
        today = get_date().strftime("%Y%m%d")

        count_today = (
            db.session.query(func.count(Transaction.id))
            .filter(func.date(Transaction.issued_at) == today)
            .scalar()
        )

        count_today += 1
        return f"INV-{today}-{count_today:04d}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
