import logging
import os
from typing import List

from Data.Recipe_stepsEntity import Recipe_stepsEntity
from Data.recipe_entity import RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular, RecipeEntity
import requests
from dotenv import load_dotenv

from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.recipe_boundary import RecipeBoundary
from config.db import collection_recipes, collection_recipes_instructions

load_dotenv()

logger = logging.getLogger("my_logger")

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
        logger.info("SpoonacularAPI initialized with base URL and API key.")

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
            logger.info(f"Found {len(recipes)} recipes by ingredients.")
            return recipes
        else:
            logger.error(
                f"Failed to find recipes by ingredients. Status code: {response.status_code}. Message: {response.json()}")
            return []

    async def find_recipe_by_id(self, recipeId: int) -> RecipeEntityByIDSpoonacular:
        url = f"{self.base_url}/recipes/{recipeId}/information?includeNutrition=false?addWinePairing=false"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recipe = RecipeEntityByIDSpoonacular(response.json())
            logger.info(f"Recipe with ID {recipeId} found.")
            return recipe
        else:
            logger.error(
                f"Failed to find recipe by ID {recipeId}. Status code: {response.status_code}. Message: {response.json()}")
            return None

    async def find_recipe_by_name(self, recipeName: str) -> List[RecipeEntity]:
        url = f"{self.base_url}/recipes/complexSearch/?query={recipeName}"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recipes = [RecipeEntity(recipe) for recipe in response.json()["results"]]
            logger.info(f"Found {len(recipes)} recipes by name '{recipeName}'.")
            return recipes
        else:
            logger.error(
                f"Failed to find recipe by name '{recipeName}'. Status code: {response.status_code}. Message: {response.json()}")
            return None

    '''Get an analyzed breakdown of a recipe's instructions. Each step is enriched with the ingredients and equipment required.'''
    async def get_analyzed_recipe_instructions(self, recipeId: int) -> List[Recipe_stepsEntity]:
        url = f"{self.base_url}/recipes/{recipeId}/analyzedInstructions"
        headers = {
            "x-api-key": self.api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recipes = [Recipe_stepsEntity(recipe_stepsEntity) for recipe_stepsEntity in response.json()]
            logger.info(f"Analyzed instructions for recipe ID {recipeId} retrieved.")
            return recipes
        else:
            logger.error(
                f"Failed to get analyzed instructions for recipe ID {recipeId}. Status code: {response.status_code}. Message: {response.json()}")
            return None

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
            target_amount = response.json().get("targetAmount")
            logger.info(f"Converted {sourceNumber} {sourceUnit} of '{ingredient_name}' to {target_amount} grams.")
            return target_amount
        else:
            logger.error(
                f"Failed to convert ingredient amount for '{ingredient_name}'. Status code: {response.status_code}. Message: {response.json()}")
            return None



class RecipesCRUD:
    def __init__(self):
        self.collection = collection_recipes
        logger.info("RecipesCRUD initialized with collection_recipes.")

    def add_recipe(self, recipe_id: str, recipe: RecipeBoundary):
        try:
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
            logger.info(f"Recipe with ID {recipe_id} added successfully.")
        except Exception as e:
            logger.error(f"Error adding recipe with ID {recipe_id}: {e}")

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundary:
        try:
            recipe_data = self.collection.find_one({"_id": recipe_id})
            if recipe_data is None:
                logger.info(f"No recipe found with ID {recipe_id}.")
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
            logger.info(f"Recipe with ID {recipe_id} retrieved successfully.")
            return recipe
        except Exception as e:
            logger.error(f"Error retrieving recipe with ID {recipe_id}: {e}")
            return None


    def delete_all_recipes(self):
        try:
            result = self.collection.delete_many({})
            logger.info(f"Deleted all recipes. Count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting all recipes: {e}")
            return 0
class RecipesInstructionsCRUD:
    def __init__(self):
        self.collection = collection_recipes_instructions
        logger.info("RecipesInstructionsCRUD initialized with collection_recipes_instructions.")

    def serialize_temperature(self, temperature):
        return {"number": temperature.number, "unit": temperature.unit} if temperature else None

    def serialize_equipment(self, equipment):
        return {
            "name": equipment.name,
            "id": equipment.id,
            "image": equipment.image,
            "temperature": self.serialize_temperature(equipment.temperature)
        }

    def serialize_ingredient(self, ingredient):
        return {
            "id": ingredient.id,
            "name": ingredient.name,
            "image": ingredient.image
        }

    def serialize_step(self, step):
        return {
            "equipments": [self.serialize_equipment(equipment) for equipment in step.equipments],
            "ingredients": [self.serialize_ingredient(ingredient) for ingredient in step.ingredients],
            "length": self.serialize_length(step.length) if step.length else None,
            "number": step.number,
            "step": step.step
        }

    def serialize_length(self, length):
        return {"number": length.number, "unit": length.unit} if length else None

    def add_recipe_instructions(self, recipe_id: str, recipe_stepsEntity_lst: List[Recipe_stepsEntity]):
        try:
            recipe_data = {
                "_id": recipe_id,
                "steps_entities": []
            }
            for entity in recipe_stepsEntity_lst:
                steps_data = [self.serialize_step(step) for step in entity.steps]
                recipe_data["steps_entities"].append({"name": entity.name, "steps": steps_data})

            self.collection.insert_one(recipe_data)
            logger.info(f"Recipe instructions for ID {recipe_id} added successfully.")
        except Exception as e:
            logger.error(f"Error adding recipe instructions for ID {recipe_id}: {e}")

    def get_recipe_instructions(self, recipe_id: str) -> List[Recipe_stepsEntity]:
        try:
            recipe_data = self.collection.find_one({"_id": recipe_id})
            if recipe_data:
                steps_entities = [Recipe_stepsEntity(entity_data) for entity_data in recipe_data.get("steps_entities", [])]
                logger.info(f"Recipe instructions for ID {recipe_id} retrieved successfully.")
                return steps_entities
            else:
                logger.info(f"No recipe instructions found for ID {recipe_id}.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving recipe instructions for ID {recipe_id}: {e}")
            return None