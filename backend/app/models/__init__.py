def orm_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

from app.models.product import Product
from app.models.recipe import Recipe
from app.models.brand_product import BrandProduct
from app.models.daily_meal_plan import DailyMealPlan
from app.models.product_category import ProductCategory
from app.models.receipt import Receipt
from app.models.receipt_item import ReceiptItem
from app.models.shopping_item import ShoppingItem
from app.models.income import Income
from app.models.expense import Expense
