import calendar
from datetime import timedelta, date

def orm_to_dict(obj):
    result = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    if "currency" in result:
        result["currency"] = result["currency"].symbol
    return result

def parse_income_expense_data(r):
    name = r.get('name')
    value = r.get('value')
    if name is None or value is None:
        return "missing name or value for new expense", 400

    date_str = r.get('date_start')
    if date_str is None:
        date_start = date.today()
    else:
        date_start = date.fromisoformat(date_str)

    date_str_end = r.get('date_end')
    date_end = None
    if date_str_end is not None:
        date_end = date.fromisoformat(date_str_end)

    recurrence = r.get("recurrence", None)
    recurrence_value = r.get("recurrence_value", None)

    return (name, value, date_start, date_end, recurrence, recurrence_value)

def items_from_recurrence_per_month(item, month):
    result = []

    _, mDays = calendar.monthrange(month.year, month.month)
    mStart = month.replace(day=1)
    mEnd = month.replace(day=mDays)

    times = item["recurrence_value"]

    if item["recurrence"] == "week":
        # TODO: add an item every X weeks
        delta = timedelta(weeks=times)
    elif item["recurrence"] == "month":
        # TODO: add an item every X months
        delta = timedelta(weeks=4*times)
    elif item["recurrence"] == "year":
        # TODO: add an item every X years
        delta = timedelta(years=times)

    date = item["date_start"]
    while date <= mEnd:
        if date >= mStart:
            result.append(item.copy())
            if item["recurrence"] == "month":
                result[-1]["date_start"] = date.replace(
                    day=get_day_in_month(date, item["date_start"].day)
                )
            elif item["recurrence"] == "year":
                result[-1]["date_start"] = date.replace(month=item["date_start"].month)
                result[-1]["date_start"] = date.replace(
                    day=get_day_in_month(date, item["date_start"].day)
                )
            else:
                result[-1]["date_start"] = date
        date = date + delta

    print(item, result)

    return result

def get_day_in_month(date, day):

    _, mDays = calendar.monthrange(date.year, date.month)

    if day <= 0:
        return 1
    if day > mDays:
        return mDays

    return day
