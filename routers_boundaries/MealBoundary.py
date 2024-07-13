from datetime import datetime
from typing import Dict

from routers_boundaries.IngredientBoundary import IngredientBoundary

meal_types = ("Breakfast", "Lunch", "Dinner", "Snacks")


class MealBoundary:
    def __init__(self, users: list[str], number_of_dishes: float):
        self.users = users
        self.number_of_dishes = number_of_dishes


class MealBoundaryWithGasPollution(MealBoundary):
    def __init__(self, mealBoundary: MealBoundary, sum_gas_pollution: Dict[str, float]):
        super().__init__(mealBoundary.users, mealBoundary.number_of_dishes)
        self.sum_gas_pollution = sum_gas_pollution
