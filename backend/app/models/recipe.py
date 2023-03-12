from app.extensions import db
from sqlalchemy_utils import URLType

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    recipe = db.Column(URLType, nullable=True)
