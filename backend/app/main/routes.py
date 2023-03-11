import datetime
from flask import jsonify, request

from app.main import bp
from app.extensions import db
from app.models.daily_meal_plan import DailyMealPlan
from app.models.recipe import Recipe
from app.models import orm_to_dict

@bp.get("/recipes")
def recipes():
    recipes = db.session.execute(db.select(Recipe)).scalars()
    return jsonify([orm_to_dict(r) for r in recipes])

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

    result = []
    for p in plan:
        obj = orm_to_dict(p)
        obj["recipe_name"] = p.recipe.name
        result.append(obj)

    return jsonify(result)

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
        recipeID = request.args.get('id', '')

        plan = db.session.execute(db.select(DailyMealPlan).filter_by(date=date)).scalar()
        recipe = db.session.execute(db.select(Recipe).filter_by(id=recipeID)).scalar()

        if recipe is None:
            return jsonify({ "error": f"recipe with ID {recipeID} does not exist" })

        if plan is not None:
            plan.recipe = recipe
        else:
            plan = DailyMealPlan(date=date, recipe=recipe)
            db.session.add(plan)

        db.session.commit()
    else:
        date = datetime.date.fromisoformat(date_str)
        plan = db.session.execute(db.select(DailyMealPlan).filter_by(date=date)).scalar()

    if plan is not None:
        result = orm_to_dict(plan)

    return jsonify(result)
