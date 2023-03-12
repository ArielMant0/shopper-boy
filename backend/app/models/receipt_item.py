from app.extensions import db
from app.models.brand_product import BrandProduct
from app.models.receipt import Receipt
from sqlalchemy_utils import CurrencyType

class ReceiptItem(db.Model):
    __tablename__ = "receipt_items"

    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(15), default="pp")
    amount = db.Column(db.Float, default=1.0)
    price = db.Column(db.Float, default=0.0)
    currency = db.Column(CurrencyType, default="EUR")

    brand_product_id = db.Column(db.Integer, db.ForeignKey(BrandProduct.id))
    receipt_id = db.Column(db.Integer, db.ForeignKey(Receipt.id))

    brand_product = db.relationship("BrandProduct", backref="receipt_items")
    receipt = db.relationship("Receipt", backref="receipt_items")
