from bson import ObjectId
from fastapi import APIRouter
from config.db import collection_pollution
from DAL.recipes_db_connection import SpoonacularAPI

router = APIRouter(prefix='/drones')
instance = SpoonacularAPI()
@router.get("/getRecipesByIngredients")
async def get_recipes(ingredients: str):
    ingredients_list = ingredients.split(',')
    instance = SpoonacularAPI.get_instance()
    return await instance.find_recipes_by_ingredients(ingredients_list)

@router.get("/")
async def get_pollution_data():
    dict = {'a':1,'b':2}
    result = collection_pollution.insert_one(dict)
    inserted_id = result.inserted_id
    inserted_drone = collection_pollution.find_one({"_id": ObjectId(inserted_id)}, {'_id': 0})
    return inserted_drone