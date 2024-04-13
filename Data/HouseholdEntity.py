from typing import List

from Data.IngredientEntity import IngredientEntity
from routers_boundaries.recipe_boundary import RecipeBoundary


class HouseholdEntity:
    def __init__(self, household_id: str, household_name: str, household_image, participants: List[str],
                 ingredients: dict, meals: dict):
        self.id = household_id
        self.name = household_name
        self.image = household_image
        self.participants = participants
        self.ingredients = ingredients
        self.meals = meals