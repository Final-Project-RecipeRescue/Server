import asyncio
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from BL.users_household_service import UsersHouseholdService, UserException, InvalidArgException, HouseholdException
from fastapi import APIRouter
router = APIRouter(prefix='/users_household', tags=['users and household operations'])  ## tag is description of router
from datetime import date
user_household_service = UsersHouseholdService()
import logging

logger = logging.getLogger("my_logger")

# Adding a new household with the user who created it
@router.post("/createNewHousehold")
async def createNewHousehold(user_mail: str, household_name: str):
    try:
        await user_household_service.create_household(user_mail, household_name)
        logger.info(f"Household '{household_name}' added successfully by user '{user_mail}'")
        return {"message": "Household added successfully"}
    except UserException as e:
        logger.error(f"Error creating household: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))
# Define the Pydantic model for the request body
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str
    state: str
# Adding a new user
@router.post("/add_user")
async def add_user(user: User):
    # Logic to add a new user
    try:
        await user_household_service.create_user(user.first_name, user.last_name, user.email, user.country, user.state)
        logger.info(f"User '{user.email}' added successfully")
        return {"message": "Successfully Added User"}
    except UserException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))
    except InvalidArgException as e:
        logger.error(f"Error adding user: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))

# Getting a user by email
@router.get("/get_user")
async def get_user(user_email: str):
    try:
        user = await user_household_service.get_user(user_email)
        logger.info(f"User '{user_email}' retrieved successfully")
        return user
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error retrieving user: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))

# Getting a household user by ID
@router.get("/get_household_user_by_id")
async def get_household_user_by_id(user_email: str, household_id: str):
    try:
        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        logger.info(f"Household '{household_id}' user retrieved successfully for user '{user_email}'")
        return household
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household user by ID: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, UserException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e.message))
# Getting a household user by name
@router.get("/get_household_user_by_name")
async def get_household_user_by_name(user_email: str, household_name: str):
    try:
        households = await user_household_service.get_household_user_by_name(user_email, household_name)
        logger.info(f"Household '{household_name}' users retrieved successfully for user '{user_email}'")
        return households
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household users by name: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, UserException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e.message))
# Adding a user to a household
@router.post("/add_user_to_household")
async def add_user_to_household(user_email: str, household_id: str):
    try:
        await user_household_service.add_user_to_household(user_email, household_id)
        logger.info(f"User '{user_email}' added to household '{household_id}' successfully")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding user to household: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))

# Adding an ingredient to a household by name
@router.post("/add_ingredient_to_household_by_ingredient_name")
async def add_ingredient_to_household_by_ingredient_name(user_email: str, household_id: str, ingredient_name: str, ingredient_amount: float):
    try:
        await user_household_service.add_ingredient_to_household_by_ingredient_name(user_email, household_id,ingredient_name,ingredient_amount)
        logger.info(f"Ingredient '{ingredient_name}' added to household '{household_id}' successfully by user '{user_email}'")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding ingredient to household by name: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e))
    except ValueError as e:
        logger.error(f"Ingredient {ingredient_name} dose not exist: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


class Ingredient (BaseModel):
    IngredientName : str  # The name of the ingredient
    IngredientAmount : float  # The amount of the ingredient in grams
class ListIngredients(BaseModel):
    ingredients: list[Ingredient]
# Adding a list of ingredients to a household
@router.post("/add_list_ingredients_to_household")
async def add_list_ingredients_to_household(user_email: str, household_id: str, list_ingredients: ListIngredients):
    # Create a list of coroutine objects for each ingredient addition
    tasks = [
        add_ingredient_to_household_by_ingredient_name(user_email, household_id, ingredient.IngredientName, ingredient.IngredientAmount)
        for ingredient in list_ingredients.ingredients
    ]

    # Run all tasks concurrently and wait for all of them to finish
    results = await asyncio.gather(*tasks)
    logger.info(f"List of ingredients added to household '{household_id}' successfully by user '{user_email}'")
    # Optionally, you can handle the results array or errors as needed
    return {"status": "success", "results": results}

'''
Remove ingredient from a certain date
'''
@router.delete("/remove_ingredient_from_household_by_date")
async def remove_ingredient_from_household_by_date(user_email: str, household_id: str, ingredient_name: str,
                                           ingredient_amount: float, year: int, month: int, day: int):
    ingredient_date = None
    try:
        # Create a date object from the provided year, month, and day
        ingredient_date = date(year, month, day)
    except ValueError:
        logger.error("Invalid date provided")
        raise HTTPException(status_code=400, detail="Invalid date provided")

    try:
        await user_household_service.remove_household_ingredient_by_date(user_email, household_id, ingredient_name,
                                                                  ingredient_amount, ingredient_date)
        logger.info(
            f"Ingredient '{ingredient_name}' in {ingredient_date} removed from household '{household_id}' successfully by user '{user_email}'")
    except InvalidArgException as e:
        logger.error(f"Error removing ingredient {ingredient_name} from household: {household_id} error : {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))

# Removing an ingredient from a household
@router.delete("/remove_ingredient_from_household")
async def remove_ingredient_from_household(user_email: str, household_id: str, ingredient_name: str,
                                           ingredient_amount: float):
    try:
        await user_household_service.remove_household_ingredient(user_email, household_id, ingredient_name,
                                                                  ingredient_amount)
        logger.info(
            f"Ingredient '{ingredient_name}' removed from household '{household_id}' successfully by user '{user_email}'")
    except InvalidArgException as e:
        logger.error(f"Error removing ingredient {ingredient_name} from household: {household_id} error : {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))

# Getting all ingredients in a household
@router.get("/get_all_ingredients_in_household")
async def get_all_ingredients_in_household(user_email: str, household_id: str):
    try:
        ingredients = await user_household_service.get_all_ingredients_in_household(user_email, household_id)
        logger.info(f"All ingredients retrieved from household '{household_id}' successfully by user '{user_email}'")
        return ingredients
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving all ingredients from household: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e.message))









'''
# Receiving the ingredients in the household
@router.get("/get_ingredients_in_household/{household_id}")
async def get_ingredients_in_household(household_id: int):
    # Logic to get ingredients in a household
    # Assume household_id validation
    household = households[household_id]
    return {"ingredients": household.get("ingredients", [])}

# Getting all the user's households
@router.get("/get_user_households/{user_id}")
async def get_user_households(user_id: int):
    # Logic to get all households of a user
    user_households = [household for household in households if user_id in household["participants"]]
    return {"user_households": user_households}

# Getting all households in the software
@router.get("/get_all_households")
async def get_all_households():
    # Logic to get all households
    return {"all_households": households}

# Acceptance of all users in the household
@router.post("/accept_all_users/{household_id}")
async def accept_all_users(household_id: int):
    # Logic to accept all users in a household
    # Assume household_id validation
    household = households[household_id]
    household["participants_accepted"] = household.get("participants", [])
    return {"message": "All users accepted in the household"}

# Setting up an additional manager for the household
@router.post("/add_manager_to_household")
async def add_manager_to_household(household_id: int, manager_id: int):
    # Logic to add a manager to a household
    # Assume household_id validation
    household = households[household_id]
    household["managers"].append(manager_id)
    return {"message": "Manager added to household"}

# Accepting all users
@router.post("/get_all_users")
async def accept_all_users():
    # Logic to accept all users
    for household in households:
        household["participants_accepted"] = household.get("participants", [])
    return {"message": "All users accepted"}

# Receiving all the recipes that the household consumed
@router.get("/get_consumed_recipes/{household_id}")
async def get_consumed_recipes(household_id: int):
    # Logic to get all consumed recipes by a household
    # Assume household_id validation
    household_recipes = [recipe for recipe in recipes_consumed if recipe["household_id"] == household_id]
    return {"consumed_recipes": household_recipes}

# Receiving all the ingredients that the household threw away in a certain period of time
@router.get("/get_thrown_away_ingredients/{household_id}")
async def get_thrown_away_ingredients(household_id: int, start_date: str, end_date: str):
    # Logic to get thrown away ingredients by a household within a certain period
    # Assume household_id validation and date parsing
    return {"thrown_away_ingredients": []}  # Placeholder for actual logic

'''
