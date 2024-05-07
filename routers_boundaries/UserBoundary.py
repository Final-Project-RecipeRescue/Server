import re
from typing import List, Optional
from routers_boundaries.MealBoundary import  MealBoundaryWithIngredients


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class UserBoundary:
    def __init__(self, first_name: str, last_name: str, user_email: str, image, households_ids: List[str],
                 meals: {str: list[MealBoundaryWithIngredients]}, country: str, state: Optional[str]):
        self.first_name = first_name
        self.last_name = last_name
        self.user_email = user_email if is_valid_email(user_email) else None
        self.image = image
        self.households = households_ids if households_ids is not None else []
        self.meals = meals
        self.country = country
        self.state = state
