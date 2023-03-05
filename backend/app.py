import os
import json
import datetime
import sqlalchemy as sa
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
CORS(app)

db = SQLAlchemy(app)

@dataclass
class DailyMealPlan(db.Model):
    __tablename__ = "daily_meal_plan"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(60), nullable=False)
    date = sa.Column(sa.Date, nullable=False)
    recipe = sa.Column(sa.String, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.get("/weekly-plan")
def weekly_plan():
    """
    Return the weekly meal plan for the 7
    days around today (-1 to +5)
    """
    today = datetime.date.today()
    from_date = today + datetime.timedelta(days=-1)
    to_date = today + datetime.timedelta(days=5)

    plan = db.session.execute(db.select(DailyMealPlan).where(DailyMealPlan.date >= from_date).where(DailyMealPlan.date <= to_date)).scalars()
    return jsonify([p.to_dict() for p in plan])

@app.post("/daily-plan")
def daily_plan():
    """
    Set the meal plan for a specific day
    """
    data = json.loads(request.data)
    print(data)

    date = datetime.date.fromisoformat(data["date"])

    plan = db.session.execute(db.select(DailyMealPlan).filter_by(date=date)).scalar()
    if plan is not None:
        plan.name = data["name"]
        plan.recipe = data["recipe"]
    else:
        plan = DailyMealPlan(name=data["name"], date=date, recipe=data["recipe"])
        db.session.add(plan)

    db.session.commit()

    return jsonify({ "success": True })

if __name__ == "__main__":
    app.run()
