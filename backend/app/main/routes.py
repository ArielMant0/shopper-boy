import datetime
from flask import jsonify, request

from app.main import bp
from app.extensions import db
from app.models.daily_meal_plan import DailyMealPlan

@bp.get("/weekly-plan")
def weekly_plan():
    """
    Return the weekly meal plan for the 7
    days around the given date (-1 to +5)
    """
    date_str = request.args.get('date')
    if date_str is None:
        selected = datetime.date.today()
    else:
        selected = datetime.date.fromisoformat(date_str)

    from_date = selected + datetime.timedelta(days=-1)
    to_date = selected + datetime.timedelta(days=5)

    plan = db.session.execute(db.select(DailyMealPlan).where(DailyMealPlan.date >= from_date).where(DailyMealPlan.date <= to_date)).scalars()
    return jsonify([p.to_dict() for p in plan])

@bp.route("/daily-plan", methods=["GET", "POST"])
def daily_plan():
    """
    Get or set the meal plan for a specific day
    """

    date_str = request.args.get('date', '')
    if len(date_str) == 0:
        return jsonify({ "error": "no date" })

    result = {}

    if request.method == "POST":
        date = datetime.date.fromisoformat(date_str)
        name = request.args.get('name', '')
        recipe = request.args.get('recipe', '')

        plan = db.session.execute(db.select(DailyMealPlan).filter_by(date=date)).scalar()
        if plan is not None:
            plan.name = name
            plan.recipe = recipe
        else:
            plan = DailyMealPlan(name=name, date=date, recipe=recipe)
            db.session.add(plan)

        print(name, recipe)

        db.session.commit()
    else:
        date = datetime.date.fromisoformat(date_str)
        plan = db.session.execute(db.select(DailyMealPlan).filter_by(date=date)).scalar()

    if plan is not None:
        result = plan.to_dict()

    return jsonify(result)
