import asyncio
import json
import os
from typing import List

from Data.Recipe_stepsEntity import Recipe_stepsEntity
from Data.recipe_entity import RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular, RecipeEntity
import requests
from dotenv import load_dotenv

from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.recipe_boundary import RecipeBoundary
from config.db import collection_recipes

load_dotenv()


# with open('DAL/spoonacular_test_by_ingredients.json', 'r') as file:
# recipes_json_by_ingredients = json.load(file)

# with open('DAL/spoonacular_test_by_ID.json', 'r') as file:
# recipes_json_by_ID = json.load(file)

class SpoonacularAPI:
    _instance = None
    api_key = None

    @staticmethod
    def get_instance():
        if SpoonacularAPI._instance is None:
            SpoonacularAPI._instance = SpoonacularAPI()
        return SpoonacularAPI._instance

    def __init__(self):
        if SpoonacularAPI._instance is not None:
            pass
            # raise Exception("Singleton instance spoonacular already exists.")
        self.base_url = "https://api.spoonacular.com"
        self.initialized = True
        self.api_key = os.getenv("SPOONACULAR_API_KEY")
        SpoonacularAPI._instance = self

    async def find_recipes_by_ingredients(self, ingredients: List[str], number=10, ranking=2, ignorePantry=True) -> \
    List[RecipeEntityByIngredientSpoonacular]:
        url = f"{self.base_url}/recipes/findByIngredients"
        headers = {
            "x-api-key": self.api_key
        }
        params = {
            "ingredients": ",".join(ingredients),
            "number": number,
            "ranking": ranking,
            "ignorePantry": ignorePantry
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            recipes = []
            for recipe in response.json():
                recipes.append(RecipeEntityByIngredientSpoonacular(recipe))
            return recipes
        else:
            print("Error:", response.status_code)
            return None

    async def find_recipe_by_id(self, recipeId: int) -> RecipeEntityByIDSpoonacular:
        url = f"{self.base_url}/recipes/{recipeId}/information?includeNutrition=false?addWinePairing=false"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return RecipeEntityByIDSpoonacular(response.json())
        else:
            return None

    async def find_recipe_by_name(self, recipeName: str) -> List[RecipeEntity]:
        url = f"{self.base_url}/recipes/complexSearch/?query={recipeName}"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recipes = []
            for recipe in response.json()["results"]:
                recipes.append(RecipeEntity(recipe))
            return recipes
        else:
            return None

    '''Get an analyzed breakdown of a recipe's instructions. Each step is enriched with the ingredients and equipment required.'''
    async def get_analyzed_recipe_instructions(self, recipeId: int) -> List[Recipe_stepsEntity]:
        url = f"{self.base_url}/recipes/{recipeId}/analyzedInstructions"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recipes = []
            for recipe_stepsEntity in response.json():
                recipes.append(Recipe_stepsEntity(recipe_stepsEntity))
            return recipes

    async def convertIngredientAmountToGrams(self, ingredient_name: str, sourceNumber: float, sourceUnit: str):
        url = (f"{self.base_url}/recipes/"
               f"convert?ingredientName={ingredient_name}"
               f"&sourceAmount={sourceNumber}&"
               f"sourceUnit={sourceUnit}&"
               f"targetUnit=grams")
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("targetAmount")


class RecipesCRUD:
    def __init__(self):
        self.collection = collection_recipes

    def add_recipe(self, recipe_id: str, recipe: RecipeBoundary):
        recipe_data = {
            "_id": recipe_id,
            "recipe_name": recipe.recipe_name,
            "ingredients": [
                {
                    "ingredient_id": ingredient.ingredient_id,
                    "name": ingredient.name,
                    "amount": ingredient.amount,
                    "unit": ingredient.unit,
                }
                for ingredient in recipe.ingredients
            ],
            "image_url": recipe.image_url
        }
        self.collection.insert_one(recipe_data)

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundary:
        recipe_data = self.collection.find_one({"_id": recipe_id})
        if recipe_data is None:
            return None

        ingredients = [
            IngredientBoundary(
                ingredient["ingredient_id"],
                ingredient["name"],
                ingredient["amount"],
                ingredient["unit"],
                None
            )
            for ingredient in recipe_data["ingredients"]
        ]

        recipe = RecipeBoundary(int(recipe_id),
                                recipe_data["recipe_name"],
                                ingredients,
                                recipe_data["image_url"]
                                )
        return recipe

    def delete_all_recipes(self):
        result = self.collection.delete_many({})
        return result.deleted_count

