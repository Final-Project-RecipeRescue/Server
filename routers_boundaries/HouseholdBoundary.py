from typing import List

from routers_boundaries import MealBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.MealBoundary import meal_types


class HouseholdBoundary:
    def __init__(self, household_id: str, household_name: str, household_image, participants: List[str],
                 ingredients: dict[str, list[IngredientBoundary]], meals: {str: {meal_types: {str: [MealBoundary]}}}):
        self.household_id = household_id
        self.household_name = household_name
        self.household_image = household_image
        self.participants = participants
        self.ingredients = ingredients
        self.meals = meals
