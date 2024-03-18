from fastapi import APIRouter

from DAL.recipes_db_connection import SpoonacularAPI

router = APIRouter(prefix='/drones')
instance = SpoonacularAPI()
@router.get("/getRecipesByIngredients")
async def get_recipes(ingredients : str):
    ingredients_list = ingredients.split(',')
    instance = SpoonacularAPI.get_instance()
    return await instance.find_recipes_by_ingredients(ingredients_list)

# Endpoint to get all drones by availability status
@router.get("/findByStatus/{status}")
async def get_drones_by_status(status):
    # drones = await drone_service.get_drones_by_status(status)
    # if not drones:
    #     raise HTTPException(status_code=404, detail=f"No drones found with status {status}")
    # return drones
    return
