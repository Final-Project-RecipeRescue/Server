from fastapi import APIRouter, HTTPException, status
import logging
from BL.recipes_service import RecipesService

router = APIRouter(prefix='/recipes', tags=['recipes'])  ## tag is description of router
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
    if ingredients.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The list of ingredients is empty")
    ingredients_list = ingredients.split(',')
    logger.debug(f"Received request to get recipes by ingredients: {ingredients_list}")
    try:
        recipes = await recipes_service.get_recipes_by_ingredients_lst(ingredients_list, True)
        if recipes is None:
            logger.info(f"From this ingredients list : {ingredients_list} there is no recipes")
            return
        logger.info("Retrieved recipes successfully")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


@router.get("/getRecipesByIngredientsWithoutMissingIngredients")
async def get_recipes_without_missing_ingredients(ingredients: str):
    ingredients_list = ingredients.split(',')
    logger.debug(f"Received request to get recipes by ingredients without missing ingredients: {ingredients_list}")
    try:
        recipes = await recipes_service.get_recipes_by_ingredients_lst(ingredients_list, False)
        if recipes is None:
            logger.info(
                f"From this ingredients list : {ingredients_list} there is no recipes without missing ingredients")
            return
        logger.info("Retrieved recipes without missing ingredients successfully")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes without missing ingredients: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


@router.get("/getRecipesByName/{recipe_name}")
async def get_recipes_by_name(recipe_name: str):
    logger.debug(f"Received request to get recipes by name: {recipe_name}")
    try:
        recipes = await recipes_service.get_recipe_by_name(recipe_name)
        if recipes is None or len(recipes) == 0:
            logger.info(f"No recipes found for the name {recipe_name}")
            return
        logger.info(f"Retrieved recipes by name: {recipe_name}")
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving recipes by name: {recipe_name}, {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.__str__())


@router.get("/getRecipeInstructions/{recipe_id}")
async def get_recipe_instructions(recipe_id: str):
    logger.debug(f"Received request to get instructions for recipe: {recipe_id}")
    try:
        instructions = await recipes_service.get_recipe_instructions(recipe_id)
        if instructions is None:
            logger.info(f"No instructions for recipe: {recipe_id}")
            return
        else:
            logger.info(f"Retrieved instructions for recipe: {recipe_id}")
        return instructions
    except Exception as e:
        logger.error(f"Error retrieving instructions for recipe: {recipe_id}, {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__str__())
