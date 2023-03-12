from app.extensions import db
from app.models.product_category import ProductCategory

CATEGORIES_DEFAULT = [
    "Obst",
    "Gemüse",
    "Backwaren",
    "Teigwaren",
    "Fisch",
    "Fleisch",
    "Milchprodukte",
    "Fertigprodukte",
    "Tierprodukte",
    "Süßigkeiten",
    "Getränke",
    "Aufstrich",
    "Aufschnitt",
    "Öl",
    "Getreide",
    "Getreideprodukte",
    "Ersatzprodukte",
    "Nüsse",
    "Hülsenfrüchte",
    "Müsli",
    "Snacks",
    "Gewürze",
    "Süßungsmittel",
    "Haushaltsprodukte",
    "Hygieneprodukte",
    "Elektronik",
    "Sonstige"
]

def add_categories(categories, clear=False):

    if clear:
        db.session.query(ProductCategory).delete()

    objs = []
    for c in categories:
        if "name" in c:
            objs.append(ProductCategory(name=c["name"]))
        else:
            objs.append(ProductCategory(name=c))

    db.session.add_all(objs)
    db.session.commit()

if __name__ == "__main__":
    add_categories(CATEGORIES_DEFAULT, True)
