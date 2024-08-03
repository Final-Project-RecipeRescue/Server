from fastapi import APIRouter, HTTPException, status
import logging

from BL.ingredient_service import IngredientService, ingredientsCRUD

router = APIRouter(prefix='/ingredients', tags=['ingredients'])  ## tag is description of router
logger = logging.getLogger("my_logger")

ingredient_service = IngredientService()

'''
This action transfers to the client all food ingredients that exist in the system
'''


@router.get("/getAllSystemIngredients")
async def getAllSystemIngredients():
    try:
        ingredients = ingredient_service.get_all_ingredients()
        logger.info("Retrieved all system ingredients")
        return ingredients
    except Exception as e:
        logger.error(f"Error in retrieving all system ingredients: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/getIngredientById")
async def getIngredientById(ingredient_id: int):
    try:
        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        logger.info("Retried ingredient")
        return ingredient
    except Exception as e:
        logger.error(f"Error in get ingredient by id : {ingredient_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/getIngredientByName")
async def getIngredientByName(ingredient_name: str):
    try:
        ingredient = ingredient_service.search_ingredient_by_name(ingredient_name)
        logger.info("Retried ingredient")
        return ingredient
    except Exception as e:
        logger.error(f"Error in get ingredient by name : {ingredient_name}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
