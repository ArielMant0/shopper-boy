from app.extensions import db
from app.models.recipe import Recipe

class DailyMealPlan(db.Model):
    __tablename__ = "daily_meal_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id))

    recipe = db.relationship("Recipe", backref="daily_meal_plans")
