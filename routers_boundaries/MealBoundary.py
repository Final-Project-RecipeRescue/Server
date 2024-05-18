from datetime import datetime

from routers_boundaries.IngredientBoundary import IngredientBoundary

meal_types = ("Breakfast", "Lunch", "Dinner", "Snakes")


class MealBoundary:
    def __init__(self, users: list[str],number_of_dishes: float):
        self.users = users
        self.number_of_dishes = number_of_dishes

