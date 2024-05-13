from fastapi import APIRouter, HTTPException, status
import logging
from DAL.IngredientsCRUD import IngredientsCRUD
from routers_boundaries.IngredientBoundary import IngredientBoundary

router = APIRouter(prefix='/ingredients', tags=['ingredients'])  ## tag is description of router
logger = logging.getLogger("my_logger")
ingredientsCRUD = IngredientsCRUD()

'''
This action transfers to the client all food ingredients that exist in the system
'''
@router.get("/getAllSystemIngredients")
async def getAllSystemIngredients():
    try:
        ingredients = []
        for ingredient in ingredientsCRUD.get_all_ingredients():
            ingredient_id = ingredient['id']
            name = ingredient['name']
            ingredients.append({"ingredient_id": ingredient_id, "name": name})
        logger.info("Retrieved all system ingredients")
        return ingredients
    except Exception as e:
        logger.error(f"Error in retrieving all system ingredients: {str(e)}")
        return  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


'''
This action returns a list of ingredients that match the provided partial name
'''
@router.get("/autocompleteIngredient")
async def autocompleteIngredient(partial_name: str):
    try:
        ingredients = []
        for ingredient in ingredientsCRUD.autocomplete_ingredient(partial_name):
            ingredient_id = ingredient['id']
            name = ingredient['name']
            ingredients.append({"ingredient_id": ingredient_id, "name": name})
        logger.info("Autocompleted ingredients")
        return ingredients
    except Exception as e:
        logger.error(f"Error in autocompleting ingredients: {str(e)}")
        return  HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
