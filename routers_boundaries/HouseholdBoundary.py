from typing import List, Dict
from routers_boundaries import MealBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.MealBoundary import meal_types
from routers_boundaries.UserBoundary import UserBoundary
import logging

logger = logging.getLogger("my_logger")

class HouseholdBoundary:
    def __init__(self, household_id: str, household_name: str, household_image, participants: List[str],
                 ingredients: dict[str, list[IngredientBoundary]], meals: {str: {meal_types: {str: [MealBoundary]}}}):
        self.household_id = household_id
        self.household_name = household_name
        self.household_image = household_image
        self.participants = participants
        self.ingredients = ingredients
        self.meals = meals

    def get_all_unique_names_ingredient(self) -> [str]:
        unique_names: [str] = []
        for ing_id, ing_s in self.ingredients.items():
            unique_names += list(set([ing.name for ing in ing_s]))
        return unique_names

    def remove_user(self, user_email: str):
        if user_email in self.participants:
            self.participants.remove(user_email)

    def add_user(self, user_email: str):
        if user_email not in self.participants:
            self.participants.append(user_email)

    def add_ingredient(self, ingredient: IngredientBoundary):
        try:
            existing_ingredients = self.ingredients[str(ingredient.ingredient_id)]
            found = False
            for ing in existing_ingredients:
                if ing.purchase_date == ingredient.purchase_date:
                    ing.amount += ingredient.amount
                    found = True
                    break
            if not found:
                existing_ingredients.append(ingredient)
        except KeyError as e:
            logger.info(f"Household {self.household_name}"
                        f" with id {self.household_id} add new ingredient {ingredient.ingredient_id} "
                        f"with name {ingredient.name}")
            self.ingredients[str(ingredient.ingredient_id)] = [ingredient]


class HouseholdBoundaryWithUsersData(HouseholdBoundary):
    def __init__(self, household: HouseholdBoundary, participants: List[UserBoundary]):
        super().__init__(
            household.household_id,
            household.household_name,
            household.household_image,
            [],
            household.ingredients,
            household.meals
        )
        self.participants = participants


class HouseholdBoundaryWithGasPollution(HouseholdBoundary):
    def __init__(self, household: HouseholdBoundary, sum_gas_pollution: Dict[str, float]):
        super().__init__(
            household.household_id,
            household.household_name,
            household.household_image,
            household.participants,
            household.ingredients,
            household.meals
        )
        self.sum_gas_pollution = sum_gas_pollution
