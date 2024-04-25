import json

from fastapi import APIRouter

from BL.recipes_service import RecipesService


router = APIRouter(prefix='/recipes',tags=['recipes'])## tag is description of router
recipes_service = RecipesService()

'''
This function is designed to provide service to the customer
 by having the customer tell the server what products he has 
 / what products he wants to make recipes with
 The function returns a list of recipes to the client
'''
@router.get("/getRecipesByIngredients")
async def get_recipes(ingredients: str):
    ingredients_list = ingredients.split(',')
    return await recipes_service.get_recipes_by_ingredients_lst(ingredients_list, missed_ingredients=True)

@router.get("/getRecipesByIngredientsWitoutMissedIngredients")
async def get_recipes(ingredients: str):
    ingredients_list = ingredients.split(',')
    return await recipes_service.get_recipes_by_ingredients_lst(ingredients_list,missed_ingredients=False)

'''
This function is designed to let the user find recipes by their ID,
 for example a user needs a recipe and wants to see the history of our recipes so he can search for a recipe by ID
 '''
@router.get("/getRecipeByID/{recipe_id}")
async def get_recipes_by_id(recipe_id: str):
    return await recipes_service.get_recipe_by_id(recipe_id)

@router.get("/getRecipesByIDs")
async def get_recipes_by_id(recipe_ids: str):
    recipe_ids_list = recipe_ids.split(',')
    return await recipes_service.get_recipe_by_ids(recipe_ids_list)

'''
This function will let the user search for a recipe freely
and return the list of recipes
'''
@router.get("/getRecipesByName/{recipe_name}")
async def get_recipes_by_name(recipe_name: str):
    return await recipes_service.get_recipe_by_name(recipe_name)
