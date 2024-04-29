from fastapi import APIRouter, HTTPException, status
import logging
from BL.recipes_service import RecipesService

router = APIRouter(prefix='/recipes',tags=['recipes'])## tag is description of router
recipes_service = RecipesService()
logger = logging.getLogger("my_logger")
'''
This function is designed to provide service to the customer
 by having the customer tell the server what products he has 
 / what products he wants to make recipes with
 The function returns a list of recipes to the client
'''
@router.get("/getRecipesByIngredients")
async def get_recipes(ingredients: str):
    ingredients_list = ingredients.split(',')
    logger.debug(f"Received request to get recipes by ingredients: {ingredients_list}")
    try:
        recipes = await recipes_service.get_recipes_by_ingredients_lst(ingredients_list, missed_ingredients=True)
        logger.info("Retrieved recipes successfully")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())

@router.get("/getRecipesByIngredientsWithoutMissedIngredients")
async def get_recipes_without_missed_ingredients(ingredients: str):
    ingredients_list = ingredients.split(',')
    logger.debug(f"Received request to get recipes by ingredients without missed ingredients: {ingredients_list}")
    try:
        recipes = await recipes_service.get_recipes_by_ingredients_lst(ingredients_list, missed_ingredients=False)
        logger.info("Retrieved recipes without missed ingredients successfully")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes without missed ingredients: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())

'''
This function is designed to let the user find recipes by their ID,
 for example a user needs a recipe and wants to see the history of our recipes so he can search for a recipe by ID
 '''
@router.get("/getRecipeByID/{recipe_id}")
async def get_recipe_by_id(recipe_id: str):
    logger.debug(f"Received request to get recipe by ID: {recipe_id}")
    try:
        recipe = await recipes_service.get_recipe_by_id(recipe_id)
        logger.info(f"Retrieved recipe by ID: {recipe_id}")
        return recipe
    except Exception as e:
        logger.error(f"Error retrieving recipe by ID: {recipe_id}, {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


@router.get("/getRecipesByIDs")
async def get_recipes_by_ids(recipe_ids: str):
    recipe_ids_list = recipe_ids.split(',')
    logger.debug(f"Received request to get recipes by IDs: {recipe_ids_list}")
    try:
        recipes = await recipes_service.get_recipe_by_ids(recipe_ids_list)
        logger.info("Retrieved recipes by IDs successfully")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes by IDs: {recipe_ids_list}, {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


'''
This function will let the user search for a recipe freely
and return the list of recipes
'''
@router.get("/getRecipesByName/{recipe_name}")
async def get_recipes_by_name(recipe_name: str):
    logger.debug(f"Received request to get recipes by name: {recipe_name}")
    try:
        recipes = await recipes_service.get_recipe_by_name(recipe_name)
        logger.info(f"Retrieved recipes by name: {recipe_name}")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes by name: {recipe_name}, {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())
