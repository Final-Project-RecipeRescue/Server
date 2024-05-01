from typing import List

import routers_boundaries.Ingredient_boundary
from routers_boundaries.recipe_boundary import RecipeBoundary
from routers_boundaries.Ingredient_boundary import ingredient_boundary


class HouseholdBoundary:
    def __init__(self, household_id: str, household_name: str, household_image, participants: List[str],
                 ingredients: dict[str,list[ingredient_boundary]], meals: List[RecipeBoundary]):
        self.household_id = household_id
        self.household_name = household_name
        self.household_image = household_image
        self.participants = participants
        self.ingredients = ingredients
        self.meals = meals
