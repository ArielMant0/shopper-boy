import json
import datetime
import calendar
from flask import jsonify, request

import app.utils as utils
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
        ((am.Income.date_start < date) & am.Income.date_end == None) |
        am.Income.date_start.between(date, end_date) |
        (am.Income.date_end.isnot(None) & (am.Income.date_start <= date) & (am.Income.date_end >= date))
    )).scalars()

def get_monthly_expenses(date):
    if date.day != 1:
        date = date.replace(day=1);

    nextMonth = (date.month + 1) % 13
    nextYear = date.year + 1 if nextMonth == 1 else date.year
    end_date = date.replace(month=nextMonth, year=nextYear)

    return db.session.execute(db.select(am.Expense).filter(
        ((am.Expense.date_start < date) & am.Expense.date_end == None) |
        am.Expense.date_start.between(date, end_date) |
        (am.Expense.date_end.isnot(None) & (am.Expense.date_start <= date) & (am.Expense.date_end >= date))
    )).scalars()

def get_brand_products(name, product, category=None, limit=None, similar=False):
    query = db.select(am.BrandProduct)
    if name is not None:
        if similar:
            query = query.filter(am.BrandProduct.name.icontains(name))
        else:
            query = query.filter_by(name=name)
    if product is not None:
        query = query.join(am.Product).filter_by(name=product)
    if category is not None:
        query = query.join(am.ProductCategory).filter_by(name=category)
    if limit is not None:
        query = query.limit(limit)

    return db.session.execute(query).scalars()

@bp.get("/balance")
def balance():

    date_str = request.args.get('date')
    if date_str is None:
        date = datetime.date.today()
    else:
        date = datetime.date.fromisoformat(date_str)
    # set to first day of the month
    date = date.replace(day=1);

    incs = [i.value for i in get_monthly_income(date)]
    exps = [i.value for i in get_monthly_expenses(date)]

    result = {
        "income": sum(incs),
        "expenses": sum(exps),
        "date": date.isoformat(),
        "title": calendar.month_name[date.month]
    }

    return jsonify(result)


@bp.route("/income", methods=["GET", "POST"])
def income():
    if request.method == "GET":
        # return all incomes for the month
        date_str = request.args.get('date')
        if date_str is None:
            date = datetime.date.today()
        else:
            date = datetime.date.fromisoformat(date_str)
        # set to first day of the month
        date = date.replace(day=1);
        incs = get_monthly_income(date)

        result = []
        incsDicts = [utils.orm_to_dict(i) for i in incs]
        for i in incsDicts:
            if i["recurrence"] is not None:
                items = utils.items_from_recurrence_per_month(i, date)
                result = result + items
            else:
                result.append(i)

        return jsonify(result)
    else:
        # get data
        data = utils.parse_income_expense_data(request.args)
        new_income = am.Income(
            name=data[0], value=data[1], date_start=data[2], date_end=data[3],
            recurrence=data[4], recurrence_value=data[5]
        )
        db.session.add(new_income)
        db.session.commit()

        return jsonify(utils.orm_to_dict(new_income))

@bp.post("/delete/<what>")
def delete_sth(what):
    if what == "expense":
        id = request.args.get("id")
        db.session.execute(db.delete(am.Expense).filter_by(id=id))
        db.session.commit()
    elif what == "shopping_item":
        id = request.args.get("id")
        db.session.execute(db.delete(am.ShoppingItem).filter_by(id=id))
        db.session.commit()

    return jsonify({ "success": 1 })

@bp.route("/expense", methods=["GET", "POST"])
def expense():
    if request.method == "GET":
        # return all expenses for the month
        date_str = request.args.get('date')
        if date_str is None:
            date = datetime.date.today()
        else:
            date = datetime.date.fromisoformat(date_str)
        # set to first day of the month
        date = date.replace(day=1);
        exps = get_monthly_expenses(date)

        result = []
        expsDicts = [utils.orm_to_dict(i) for i in exps]
        for i in expsDicts:
            if i["recurrence"] is not None:
                items = utils.items_from_recurrence_per_month(i, date)
                result = result + items
            else:
                result.append(i)

        return jsonify(result)
    else:
        # get data
        data = utils.parse_income_expense_data(request.args)
        new_expense = am.Expense(
            name=data[0], value=data[1], date_start=data[2], date_end=data[3],
            recurrence=data[4], recurrence_value=data[5]
        )
        db.session.add(new_expense)
        db.session.commit()

        return jsonify(utils.orm_to_dict(new_expense))


@bp.get("/categories")
def categories():
    categories = db.session.execute(db.select(am.ProductCategory)).scalars()
    return jsonify([r.name for r in categories])

@bp.route("/product", methods=["GET", "POST"])
def product():
    if request.method == "POST":
        name = request.args.get("name")
        category = request.args.get("category")
        if not name or not category:
            return { "error": "missing name or category" }

        cat = db.session.execute(db.select(am.ProductCategory).filter_by(name=category)).scalar()
        if not cat:
            cat = am.ProductCategory(name=category)
            db.session.add(cat)

        obj = am.Product(name=name, category=cat)
        db.session.add(obj)
        db.session.commit()

        return jsonify({ "success": "saldals" })
    else:
        name = request.args.get("name")
        category = request.args.get("category")
        if not name:
            return { "error": "missing name" }

        query = db.select(am.Product).filter_by(name=name)
        if category is not None:
            query = query.join(am.ProductCategory).filter_by(name=category)

        prod = db.session.execute(query).scalar()
        if prod:
            return jsonify({
                "name": prod.name,
                "category": prod.category.name,
                "price": 0.99,
                "unit": "Stk",
                "amount": 1
            })
        return jsonify({ "error": "no matching prodcut found" })

@bp.get("/products")
def products():
    name = request.args.get("name")
    category = request.args.get("category")
    limit = request.args.get("limit")
    if not name:
        return { "error": "missing name" }

    query = db.select(am.Product).filter(am.Product.name.contains(name))
    if category is not None:
        query = query.join(am.ProductCategory).filter_by(name=category)
    if limit is not None:
        query = query.limit(int(limit))

    prods = db.session.execute(query).scalars()

    results = []
    for p in prods:
        if p.category:
            results.append({
                "name": p.name,
                "category": p.category.name,
                "price": 0.99,
                "unit": "Stk",
                "amount": 1
            })

    return jsonify(results)

@bp.get("/products_list")
def products_list():
    categories = db.session.execute(db.select(am.ProductCategory)).scalars()
    results = []
    for c in categories:
        prods = db.session.execute(db.select(am.Product).filter_by(category=c).limit(10)).scalars()
        for p in prods:
            # TODO
            results.append({
                "name": p.name,
                "category": c.name,
                "price": 0.99,
                "unit": "Stk",
                "amount": 1
            })
    return jsonify(results)

@bp.get("/units")
def units():
    return jsonify(["Stk", "g", "kg", "ml", "l", "Msp.", "TL", "EL"])

@bp.route("/receipt", methods=["GET", "POST"])
def receipt():
    if request.method == "POST":
        data = json.loads(request.data)
        # add a new receipt
        items = data["items"]
        if items is None or len(items) == 0:
            return jsonify({ "error": "receipt is missing items" })

        price = 0
        for i in items:
            price += i["price"]

        date = datetime.date.fromisoformat(data["date"]) if "date" in data else datetime.date.today()
        time = datetime.time.fromisoformat(data["time"]) if "time" in data else datetime.time(18)
        dt = datetime.datetime.combine(date, time)
        print(dt)

        store_chain = data["store_chain"] if "store_chain" in data else "EDEKA"
        store_address = data["store_address"] if "store_address" in data else "Hauptstr. 5, 70563 Stuttgart"

        all_db_items = []

        expense = am.Expense(name="Einkauf", value=price, date_start=date)
        receipt = am.Receipt(
            datetime=dt,
            store_chain=store_chain,
            store_address=store_address,
            expense=expense
        )
        all_db_items.append(expense)
        all_db_items.append(receipt)

        for i in items:
            if "product" in i and len(i["product"]) > 0:
                bp_obj = db.session.execute(db.select(am.BrandProduct).filter_by(name=i["product"])).scalar()
                if bp_obj:
                    all_db_items.append(am.ReceiptItem(
                        unit=i["unit"], price=i["price"], amount=i["amount"],
                        brand_product=bp_obj, receipt=receipt
                    ))
            elif "name" in i and len(i["name"]) > 0:
                p_obj = db.session.execute(db.select(am.Product).filter_by(name=i["name"])).scalar()
                if p_obj:
                    all_db_items.append(am.ReceiptItem(
                        unit=i["unit"], price=i["price"], amount=i["amount"],
                        product=p_obj, receipt=receipt
                    ))


        db.session.add_all(all_db_items)
        db.session.execute(db.delete(am.ShoppingItem))
        db.session.commit()

        return jsonify(utils.orm_to_dict(receipt))
    # else:
        # get a specific receipt

@bp.route("/brandproduct", methods=["GET", "POST"])
def brandproduct():

    product = request.args.get("product")
    name = request.args.get("name")
    category = request.args.get("category")
    similar = request.args.get("similar", False)

    if request.method == "GET":
        bp = get_brand_products(name, product, category, similar=similar)
        return jsonify(utils.orm_to_dict(bp[0]) if bp else { "error": "brand product does not exist" })
    else:
        if name is None or product is None:
            return jsonify({ "error": "missing name or product (category)" })

        p_obj = db.session.execute(db.select(am.Product).filter_by(name=product)).scalar()

        if p_obj is None:
            if category is None:
                return jsonify({ "error": "cannot create product - missing category" })

            c_obj = db.session.execute(db.select(am.ProductCategory).filter_by(name=category)).scalar()
            if c_obj is None:
                c_obj = am.ProductCategory(name=category)
                db.session.add(c_obj)
            p_obj = am.Product(name=product, category_id=c_obj.id)
            db.session.add(p_obj)

        bp = am.BrandProduct(name=name, product_id=p_obj.id)
        db.session.add(bp)
        db.session.commit()

        return jsonify(utils.orm_to_dict(bp))

@bp.get("/brandproducts")
def brandproducts():

    product = request.args.get("product")
    name = request.args.get("name")
    category = request.args.get("category")
    limit = request.args.get("limit")
    if limit is not None:
        limit = int(limit)

    bps = get_brand_products(name, product, category, limit)

    return jsonify([utils.orm_to_dict(d) for d in bps])

@bp.get("/recipes")
def recipes():
    recipes = db.session.execute(db.select(am.Recipe)).scalars()
    return jsonify([utils.orm_to_dict(r) for r in recipes])

@bp.route("/shopping_list", methods=["GET", "POST"])
def shopping_list():
    if request.method == "GET":
        items = db.session.execute(db.select(am.ShoppingItem)).scalars()
        json_items = []
        for i in items:
            cat = ""
            if i.brand_product:
                cat = i.brand_product.product.category.name
            else:
                cat = i.product.category.name

            obj = {
                "id": i.id,
                "name": i.brand_product.name if i.brand_product else i.product.name,
                "product": i.brand_product.name if i.brand_product else "",
                "price": i.price,
                "unit": i.unit,
                "amount": i.amount,
                "cart": i.cart,
                "currency": i.currency.name,
                "category": cat
            }
            json_items.append(obj)
        return jsonify(json_items)
    else:
        data = json.loads(request.data)
        items = data["items"] if "items" in data else []

        if len(items) > 0:
            item_objs = []
            for i in items:
                use_bp = "product" in i and len(i["product"]) > 0
                if use_bp:
                    p_obj = db.session.execute(db.select(am.BrandProduct).filter_by(name=i["product"])).scalar()
                else:
                    p_obj = db.session.execute(db.select(am.Product).filter_by(name=i["name"])).scalar()

                if p_obj is None:
                    continue

                if use_bp:
                    item_objs.append(am.ShoppingItem(
                        unit=i["unit"], price=i["price"],
                        amount=i["amount"], brand_product_id=p_obj.id
                    ))
                else:
                    item_objs.append(am.ShoppingItem(
                        unit=i["unit"], price=i["price"],
                        amount=i["amount"], product_id=p_obj.id
                    ))
            db.session.add_all(item_objs)
            db.session.commit()

            return jsonify({ "count": len(item_objs) })

@bp.route("/shopping_item", methods=["GET", "POST"])
def shopping_item():
    if request.method == "POST":
        data = json.loads(request.data)

        # only update if id is present
        if "id" in data:
            obj = db.session.execute(db.select(am.ShoppingItem).filter_by(id=data["id"])).scalar()
            if obj:
                obj.price = data["price"]
                obj.cart = data["cart"]
                obj.amount = data["amount"]
                obj.unit = data["unit"]
                # TODO: brand product?

        # otherwise insert
        else:
            if "name" not in data:
                return { "error": "missing product" }

            p_obj = db.session.execute(db.select(am.Product).filter_by(name=data["name"])).scalar()
            if p_obj is None:
                return { "error": "product does not exist" }

            obj = am.ShoppingItem(
                price=data["price"], amount=data["amount"],
                unit=data["unit"], cart=data["cart"], product=p_obj
            )

            db.session.add(p_obj)
            db.session.add(obj)

        db.session.commit()

    return { "success": "hllo" }


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
        obj = utils.orm_to_dict(p)
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
        result = utils.orm_to_dict(plan)

    return jsonify(result)
