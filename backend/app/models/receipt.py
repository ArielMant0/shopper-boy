from datetime import datetime
from app.extensions import db

class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float, nullable=False)
    store_chain = db.Column(db.String)
    store_address = db.Column(db.String)
