import datetime
import functools
import calendar
from flask import jsonify, request

from app.main import bp
from app.extensions import db
import app.models as am

def get_monthly_income(date):
    if date.day != 1:
        date = date.replace(day=1);

    nextMonth = (date.month + 1) % 13
    nextYear = date.year + 1 if nextMonth == 1 else date.year
    end_date = date.replace(month=nextMonth, year=nextYear)

    # TODO: let database calc the sum
    return db.session.execute(db.select(am.Income).filter(
        am.Income.date_start.between(date, end_date) |
        (am.Income.date_end.isnot(None) & (am.Income.date_start <= date) & (am.Income.date_end >= date))
    )).scalars()

def get_monthly_expenses(date):
    nextMonth = (date.month + 1) % 13
    nextYear = date.year + 1 if nextMonth == 1 else date.year
    end_date = date.replace(month=nextMonth, year=nextYear)

    # TODO: let database calc the sum
    return db.session.execute(db.select(am.Expense).filter(
        am.Expense.date_start.between(date, end_date) |
        (am.Expense.date_end.isnot(None) & (am.Expense.date_start <= date) & (am.Expense.date_end >= date))
    )).scalars()

@bp.get("/balance")
def balance():

    date = request.args.get('date')
    if date is None:
        date = datetime.date.today()

    # set to first day of the month
    date = date.replace(day=1);

    incs = get_monthly_income(date)
    exps = get_monthly_expenses(date)

    result = [{
        "income": functools.reduce(lambda a, b: a.value + b.value, incs, 0),
        "expenses": functools.reduce(lambda a, b: a.value + b.value, exps, 0),
        "date": date.isoformat(),
        "title": calendar.month_name[date.month]
    }]

    return jsonify(result)


@bp.route("/income", methods=["GET", "POST"])
def income():
    if request.method == "GET":
        # return all incomes for the month
        date = request.args.get('date')
        if date is None:
            date = datetime.date.today()
        # set to first day of the month
        date = date.replace(day=1);
        incs = get_monthly_income(date)
        results = [am.orm_to_dict(i) for i in incs]
        return jsonify(results)
    else:
        # get data
        name = request.args.get('name')
        value = request.args.get('value')
        if name is None or value is None:
            return "missing name or value for new income", 400

        date_start = request.args.get('date')
        if date_start is None:
            date_start = datetime.date.today()

        new_income = am.Income(name=name, value=value, date_start=date_start)
        db.session.add(new_income)
        db.session.commit()

        return jsonify(am.orm_to_dict(new_income))


@bp.get("/categories")
def categories():
    categories = db.session.execute(db.select(am.ProductCategory)).scalars()
    return jsonify([r.name for r in categories])

@bp.get("/products")
def products():
    products = db.session.execute(db.select(am.Product)).scalars()
    results = []
    for r in products:
        obj = am.orm_to_dict(r)
        cat = db.session.execute(db.select(am.ProductCategory).filter_by(id=r.category_id)).scalar()
        if cat:
            obj["category"] = cat.name
            results.append(obj)
    return jsonify(results)

@bp.get("/recipes")
def recipes():
    recipes = db.session.execute(db.select(am.Recipe)).scalars()
    return jsonify([am.orm_to_dict(r) for r in recipes])

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

    plan = db.session.execute(db.select(am.DailyMealPlan).where(am.DailyMealPlan.date >= from_date).where(am.DailyMealPlan.date <= to_date)).scalars()

    result = []
    for p in plan:
        obj = am.orm_to_dict(p)
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

        plan = db.session.execute(db.select(am.DailyMealPlan).filter_by(date=date)).scalar()
        recipe = db.session.execute(db.select(am.Recipe).filter_by(id=recipeID)).scalar()

        if recipe is None:
            return jsonify({ "error": f"recipe with ID {recipeID} does not exist" })

        if plan is not None:
            plan.recipe = recipe
        else:
            plan = am.DailyMealPlan(date=date, recipe=recipe)
            db.session.add(plan)

        db.session.commit()
    else:
        date = datetime.date.fromisoformat(date_str)
        plan = db.session.execute(db.select(am.DailyMealPlan).filter_by(date=date)).scalar()

    if plan is not None:
        result = am.orm_to_dict(plan)

    return jsonify(result)
