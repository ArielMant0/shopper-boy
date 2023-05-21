from app.extensions import db
from sqlalchemy_utils import CurrencyType

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    currency = db.Column(CurrencyType, default="EUR")
    date_start = db.Column(db.Date, nullable=False)

    date_end = db.Column(db.Date, nullable=True)
    recurrence = db.Column(db.String(15), nullable=True)
    recurrence_value = db.Column(db.Integer, nullable=True)

    _receipts = db.relationship("Receipt", backref="expenses", cascade="all, delete")
