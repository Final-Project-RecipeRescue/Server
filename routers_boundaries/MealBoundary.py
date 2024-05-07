from datetime import datetime

meal_types = ("Breakfast", "Lunch", "Dinner", "Snakes")


class MealBoundary:
    def __init__(self, used_date: datetime.date, mealType: meal_types, users: list[str], recipe_id: str,
                 number_of_dishes: float):
        self.type = mealType
        self.users = users
        self.recipe_id = recipe_id
        self.number_of_dishes = number_of_dishes
        if used_date is None:
            self.used_date = None
        else:
            self.used_date = used_date.strftime("%Y-%m-%d") if used_date else datetime.now().strftime(
                "%Y-%m-%d")


class Ing:
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount


class MealBoundaryWithIngredients(MealBoundary):
    def __init__(self, used_date: datetime.date, mealType: meal_types, users: list[str], recipe_id: str,
                 number_of_dishes: float, ingredients: list[Ing]):
        super().__init__(used_date, mealType, users, recipe_id, number_of_dishes)
        self.ingredients = ingredients
