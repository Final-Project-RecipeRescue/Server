from typing import Optional

from pydantic import BaseModel


class UserInputForAddUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str
    state: Optional[str]


class IngredientInput(BaseModel):
    IngredientName: str  # The name of the ingredient
    IngredientAmount: float  # The amount of the ingredient in grams


class ListIngredientsInput(BaseModel):
    ingredients: list[IngredientInput]


class IngredientToRemoveByDateInput(BaseModel):
    ingredient_data: IngredientInput
    year: int
    mount: int
    day: int


class MealInput(BaseModel):
    recipe_id: str
    meal_type: str
    dishes_num: float
    ingredients: list[IngredientInput]
