from app.extensions import db
from app.models.brand_product import BrandProduct
from app.models.product import Product
from app.models.receipt import Receipt
from sqlalchemy_utils import CurrencyType

class ReceiptItem(db.Model):
    __tablename__ = "receipt_items"

    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(15), default="pp")
    amount = db.Column(db.Float, default=1.0)
    price = db.Column(db.Float, default=0.0)
    currency = db.Column(CurrencyType, default="EUR")

    brand_product_id = db.Column(db.Integer, db.ForeignKey(BrandProduct.id), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    receipt_id = db.Column(db.Integer, db.ForeignKey(Receipt.id, ondelete='CASCADE'))
