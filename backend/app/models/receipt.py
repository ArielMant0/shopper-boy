from datetime import datetime
from app.extensions import db
from app.models.expense import Expense

class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    store_chain = db.Column(db.String, nullable=True)
    store_address = db.Column(db.String, nullable=True)

    expense_id = db.Column(db.Integer, db.ForeignKey(Expense.id))

    expense = db.relationship("Expense", backref="receipts")
