from app.extensions import db
from app.models.product import Product
from app.models.brand_product import BrandProduct
from sqlalchemy_utils import CurrencyType

class ShoppingItem(db.Model):
    __tablename__ = "shopping_items"

    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(15), default="pp")
    amount = db.Column(db.Float, default=1.0)
    price = db.Column(db.Float, default=0.0)
    currency = db.Column(CurrencyType, default="EUR")

    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    brand_product_id = db.Column(db.Integer, db.ForeignKey(BrandProduct.id), nullable=True)

