from app.extensions import db
from app.models.product_category import ProductCategory

class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = (
        db.UniqueConstraint('name', 'category_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(ProductCategory.id, ondelete="CASCADE"))

    category = db.relationship("ProductCategory", backref="products")
