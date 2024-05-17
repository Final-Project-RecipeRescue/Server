from typing import Optional

from pydantic import BaseModel


class UserInputForAddUser(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str
    state: Optional[str]


class IngredientInput(BaseModel):
    ingredient_id: Optional[str]
    name: str  # The name of the ingredient
    amount: float  # The amount of the ingredient in grams
    unit: Optional[str]


class ListIngredientsInput(BaseModel):
    ingredients: list[IngredientInput]


class IngredientToRemoveByDateInput(BaseModel):
    ingredient_data: IngredientInput
    year: int
    mount: int
    day: int


class RecipeInput(BaseModel):
    recipe_id: int
    recipe_name: str
    ingredients: list[IngredientInput]


class MealInput(BaseModel):
    meal_type: str
    dishes_num: float
    recipe: RecipeInput
