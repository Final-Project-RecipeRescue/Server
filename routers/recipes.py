from typing import List

from bson import ObjectId
from fastapi import APIRouter
from config.db import collection_pollution
from DAL.recipes_db_connection import SpoonacularAPI

router = APIRouter(prefix='/drones')
instance = SpoonacularAPI()

'''
This function is designed to provide service to the customer
 by having the customer tell the server what products he has 
 / what products he wants to make recipes with
 The function returns a list of recipes to the client
'''
@router.get("/getRecipesByIngredients")
async def get_recipes(ingredients: str):
    ingredients_list = ingredients.split(',')
    instance = SpoonacularAPI.get_instance()
    return await instance.find_recipes_by_ingredients(ingredients_list)
'''
This function is designed to let the user find recipes by their ID,
 for example a user needs a recipe and wants to see the history of our recipes so he can search for a recipe by ID
 '''
@router.get("/getRecipesByID/{recipe_id}")
async def get_recipes_by_id(recipe_id: str):
    return

'''
This function will let the user search for a recipe freely
and return the list of recipes
'''
@router.get("/getRecipesByName/{recipe_name}")
async def get_recipes_by_name(recipe_name: str):
    return