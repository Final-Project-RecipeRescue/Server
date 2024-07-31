import logging
import re
from typing import List, Optional, Dict
from routers_boundaries.MealBoundary import MealBoundary, meal_types, MealBoundaryWithGasPollution

logger = logging.getLogger("my_logger")

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class UserBoundary:
    def __init__(self, first_name: str, last_name: str, user_email: str, image: str, households_ids: List[str],
                 meals: {str: {meal_types: {str: MealBoundary}}}, country: str, state: Optional[str]):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email if is_valid_email(user_email) else None
        self.image = image
        self.households = households_ids if households_ids is not None else []
        self.meals = meals
        self.country = country
        self.state = state

    def remove_household(self, household_id: str):
        if household_id in self.households:
            self.households.remove(household_id)

    def add_household(self, household_id: str):
        if household_id not in self.households:
            self.households.append(household_id)
    def add_meal(self, new_meal: MealBoundary, meal_date: str, mealType: meal_types,
                 recipe_id: str):
        if not self.meals:
            self.meals = {}
        try:
            date_meals = self.meals[meal_date]
            try:
                type_meals = date_meals[mealType]
                try:
                    meal = type_meals[recipe_id]
                    meal.number_of_dishes += new_meal.number_of_dishes
                    if isinstance(meal, MealBoundaryWithGasPollution) and isinstance(new_meal,
                                                                                     MealBoundaryWithGasPollution):
                        for gas in new_meal.sum_gas_pollution.keys():
                            try:
                                meal.sum_gas_pollution[gas] += new_meal.sum_gas_pollution[gas]
                            except KeyError:
                                meal.sum_gas_pollution[gas] = new_meal.sum_gas_pollution[gas]
                except KeyError:
                    type_meals[recipe_id] = new_meal
            except KeyError:
                date_meals[mealType] = {recipe_id: new_meal}
        except KeyError:
            self.meals[meal_date] = {mealType: {recipe_id: new_meal}}


class UserBoundaryWithGasPollution(UserBoundary):
    def __init__(self, userBoundary: UserBoundary, sum_gas_pollution: Dict[str, float]):
        super().__init__(
            userBoundary.first_name,
            userBoundary.last_name,
            userBoundary.user_email,
            userBoundary.image,
            userBoundary.households,
            userBoundary.meals,
            userBoundary.country,
            userBoundary.state
        )
        self.sum_gas_pollution = sum_gas_pollution

    def update_gas_pollution(self, gas_pollution):
        try:
            for gas, pollution in gas_pollution.items():
                try:
                    self.sum_gas_pollution[gas] = self.sum_gas_pollution.get(gas, 0) + pollution
                except KeyError:
                    self.sum_gas_pollution[gas] = pollution
                logger.debug(f"Add to {gas} : {pollution} to user {self.user_email}")
        except KeyError:
            self.sum_gas_pollution = gas_pollution
