from dataclasses import dataclass
from app.extensions import db

@dataclass
class DailyMealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    date = db.Column(db.Date, nullable=False)
    recipe = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
