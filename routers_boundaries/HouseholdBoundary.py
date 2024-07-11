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

    def remove_ingredient_by_date(self, ingredient_to_remove: IngredientBoundary):
        from BL.users_household_service import InvalidArgException
        lst = self.ingredients[str(ingredient_to_remove.ingredient_id)]
        try:
            for ing in lst:
                if ing.purchase_date == ingredient_to_remove.purchase_date:
                    if ingredient_to_remove.amount > ing.amount:
                        m = (f"The amount you wanted to remove from the household {self.household_name}"
                             f" is greater than the amount that is in ingredient "
                             f"{ingredient_to_remove.name} on this date. "
                             f"The maximum amount is {ing.amount}")
                        logger.error(m)
                        raise InvalidArgException(m)
                    if ing.amount >= ingredient_to_remove.amount:
                        ing.amount -= ingredient_to_remove.amount
                    if ing.amount <= 0:
                        self._remove_ingredient(ing)
                    return
            exp = InvalidArgException(
                f"No such ingredient '{ingredient_to_remove.name}' in household '{self.household_name}' with date "
                f"{ingredient_to_remove.purchase_date}")
            logger.info(exp.message)
            raise exp
        except (KeyError, ValueError, InvalidArgException) as e:
            raise InvalidArgException(f"No such ingredient {ingredient_to_remove.name} : "
                                      f"{ingredient_to_remove.ingredient_id} "
                                      f"in household {self.household_name} : {self.household_id}")

    def _remove_ingredient(self, ingredient: IngredientBoundary):
        self.ingredients[str(ingredient.ingredient_id)].remove(ingredient)


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
