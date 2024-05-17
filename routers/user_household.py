import asyncio
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from BL.users_household_service import UsersHouseholdService, UserException, InvalidArgException, HouseholdException
from fastapi import APIRouter
from routers_boundaries.HouseholdBoundary import HouseholdBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.MealBoundary import meal_types
from routers_boundaries.InputsForApiCalls import (UserInputForAddUser, IngredientInput
, IngredientToRemoveByDateInput, ListIngredientsInput)
from routers_boundaries.UserBoundary import UserBoundary
from routers.recipes import get_recipes_without_missed_ingredients, get_recipes

router = APIRouter(prefix='/users_household', tags=['users and household operations'])  ## tag is description of router
from datetime import date
import logging

user_household_service = UsersHouseholdService()

logger = logging.getLogger("my_logger")


# Adding a new household with the user who created it
@router.post("/createNewHousehold")
async def createNewHousehold(user_mail: str, household_name: str, ingredients: Optional[ListIngredientsInput]):
    try:
        logger.info(f"Creating new household with ingredients : {ingredients.ingredients} and name : {household_name}")
        household_id = await user_household_service.create_household(user_mail, household_name)
        if ingredients is not None:
            await add_list_ingredients_to_household(user_mail, household_id, ingredients)
        logger.info(f"Household '{household_name}' added successfully by user '{user_mail}'")
        return {"message": "Household added successfully", 'household_id': household_id}
    except UserException as e:
        logger.error(f"Error creating household: {e.message}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))
    except InvalidArgException as e:
        logger.error(f"Error getting user: {e}")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


@router.delete("/delete_household")
async def delete_household_by_id(household_id: str):
    try:
        logger.info(f"Try to delete household '{household_id}'")
        await user_household_service.delete_household(household_id)
        logger.info(f"Household deleted successfully")
    except HouseholdException as e:
        logger.error(f"Error deleting household: {e.message}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Adding a new user
@router.post("/add_user")
async def add_user(user: UserInputForAddUser):
    # Logic to add a new user
    try:
        await user_household_service.create_user(user.first_name, user.last_name, user.email, user.country,
                                                 user.state)
        logger.info(f"User '{user.email}' added successfully")
        return {"message": "Successfully Added User"}
    except UserException as e:
        logger.error(f"Error creating user: {e.message}")
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


@router.delete("/delete_user")
async def delete_user(user_email: str):
    try:
        logger.info(f"Try to delete user '{user_email}'")
        await user_household_service.delete_user(user_email)
        logger.info(f"Deleted user '{user_email}'")
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error retrieving user: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Getting a household user by ID
@router.get("/get_household_user_by_id")
async def get_household_user_by_id(user_email: str, household_id: str):
    try:
        logger.info(f"Looking for user with '{user_email}' and '{household_id}'...")
        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        logger.info(f"Household '{household_id}' user retrieved successfully for user '{user_email}'")
        return household
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household user by ID: '{household_id}'")
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


@router.get("/get_all_household_details_by_user_mail")
async def get_all_household_details_by_user_mail(user_email: str):
    user = await get_user(user_email)
    if isinstance(user, HTTPException):
        return user

    households = []
    if isinstance(user, UserBoundary):
        for _ in user.households:
            try:
                household_details = await get_household_user_by_id(user_email, _)
                if isinstance(household_details, HouseholdBoundary):
                    households.append(household_details)
            except Exception as e:
                pass
    return households


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
async def add_ingredient_to_household_by_ingredient_name(user_email: str, household_id: str,
                                                         ingredient: IngredientInput):
    logger.info(f"ingredient: {ingredient.name} : {ingredient.amount}")
    try:
        await user_household_service.add_ingredient_to_household_by_ingredient_name(user_email, household_id,
                                                                                    ingredient.name,
                                                                                    ingredient.amount)
        logger.info(
            f"Ingredient '{ingredient.name}' added to household '{household_id}' successfully by user "
            f"'{user_email}'")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding ingredient to household by name: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e))
    except ValueError as e:
        logger.error(f"Ingredient {ingredient.name} dose not exist: {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Adding a list of ingredients to a household
@router.post("/add_list_ingredients_to_household")
async def add_list_ingredients_to_household(user_email: str, household_id: str, list_ingredients: ListIngredientsInput):
    # Create a list of coroutine objects for each ingredient addition
    tasks = [
        add_ingredient_to_household_by_ingredient_name(user_email, household_id, ingredient)
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
async def remove_ingredient_from_household_by_date(user_email: str, household_id: str,
                                                   ingredient: IngredientToRemoveByDateInput):
    ingredient_date = None
    try:
        # Create a date object from the provided year, month, and day
        ingredient_date = date(ingredient.year, ingredient.mount, ingredient.day)
    except ValueError:
        logger.error("Invalid date provided")
        return HTTPException(status_code=400, detail="Invalid date provided")

    try:
        await user_household_service.remove_household_ingredient_by_date(user_email,
                                                                         household_id,
                                                                         ingredient.ingredient_data.name,
                                                                         ingredient.ingredient_data.amount,
                                                                         ingredient_date)
        logger.info(
            f"Ingredient '{ingredient.ingredient_data.IngredientName}' in {ingredient_date}"
            f" removed from household '{household_id}' successfully by user '{user_email}'")
    except InvalidArgException as e:
        logger.error(f"Error removing ingredient {ingredient.ingredient_data.IngredientName}"
                     f" from household: {household_id} error : {e}")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Removing an ingredient from a household
@router.delete("/remove_ingredient_from_household")
async def remove_ingredient_from_household(user_email: str, household_id: str, ingredient: IngredientInput):
    try:
        await user_household_service.remove_household_ingredient(user_email, household_id, ingredient.name,
                                                                 ingredient.amount)
        logger.info(
            f"Ingredient '{ingredient.name}' "
            f"removed from household '{household_id}' successfully by user '{user_email}'")
    except InvalidArgException as e:
        logger.error(f"Error removing ingredient"
                     f" {ingredient.name} from household: {household_id} error : {e}")
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


@router.post("/use_recipe_by_recipe_id")
async def use_recipe_by_recipe_id(user_email: str, household_id: str,
                                  meal: str, dishes_num: float,recipe_id: str):
    try:
        mealT = None
        for meal_type in meal_types:
            if meal_type == meal:
                mealT = meal_type
        if mealT is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail=f"Invalid meal meals type is : {meal_types}")
        await user_household_service.use_recipe(user_email, household_id,mealT,dishes_num,recipe_id)
    except (UserException, InvalidArgException, HouseholdException) as e:
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status_code, detail=str(e.message))
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/get_meal_types")
def get_meal_types():
    return [f'{meal_type}' for meal_type in meal_types]


@router.get("/get_all_recipes_that_household_can_make")
async def get_all_recipes_that_household_can_make(user_email: str, household_id: str):
    ingredients_dict = await get_all_ingredients_in_household(user_email, household_id)
    ingredients_str = ""
    for ingredient_id, ingredients in ingredients_dict.items():
        unique_names = list(set([ing.name for ing in ingredients]))
        ingredients_str += ", ".join(unique_names) + ", "  # Accumulate ingredients
    ingredients_str = ingredients_str.rstrip(', ')  # Remove the trailing comma and space
    recipes = await get_recipes_without_missed_ingredients(ingredients_str)
    return recipes
