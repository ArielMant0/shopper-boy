from app.extensions import db
from app.models.recipe import Recipe

RECIPES_DEFAULT = [
    "Chili con Quinoa",
    "Pesto-Nudeln",
    "Pizza",
    "TK-Pizza",
    "Ofengemüse",
    "Asia-Nudeln",
    "Salat",
    "Nudeln mit Erbsen in Tomatensugo",
    "Kartoffel-Rosenkohl-Auflauf",
    "Veganer Kartoffelsalat",
    "Gnocchi",
    "Schupfnudeln",
    "Brötchen",
    "Linseneintopf",
    "Ramen",
    "Suppe",
    "Tortellini",
    "Flammkuchen",
    "Brot",
    "Nudeln mit Sonnenblumenhack",
    "Kichererbsencurry",
    "Kartoffelrösti",
    "Pfannkuchen",
    "Pizzabrötchen",
    "Kürbisrisotte mit Rosenkohl",
    "Sushi",
    "Raclette",
    "Kartoffeleintopf",
    "Erbseneintopf",
    "Semmelknödel",
    "Milchreis",
    "Obstsalat",
    "Ofenpaprika",
    "Falsche Gulaschsuppe",
    "Brezel",
    "Wraps"
]

def add_recipes(recipes, clear=False):

    if clear:
        db.session.query(Recipe).delete()

    objs = []
    for r in recipes:
        if "name" in r:
            if "url" in r:
                objs.append(Recipe(name=r["name"], url=r["url"]))
            else:
                objs.append(Recipe(name=r["name"]))
        else:
            objs.append(Recipe(name=r))

    db.session.add_all(objs)
    db.session.commit()

if __name__ == "__main__":
    add_recipes(RECIPES_DEFAULT, True)
