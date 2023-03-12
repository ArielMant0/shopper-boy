from app.extensions import db
from app.models.product import Product

class BrandProduct(db.Model):
    __tablename__ = "brand_products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    price_in_kg = db.Column(db.Float, default=0.0)
    price_in_pp = db.Column(db.Float, default=0.0)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id))

    product = db.relationship("Product", backref="brand_products")
