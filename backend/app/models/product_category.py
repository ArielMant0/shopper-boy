from app.extensions import db

class ProductCategory(db.Model):
    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    _products = db.relationship("Product", backref="product_categories", cascade="all, delete")
