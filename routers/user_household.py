import asyncio
import os
import time
from typing import Optional, List, Dict
from fastapi import HTTPException, status
from BL.recipes_service import RecipesService
from BL.users_household_service import UsersHouseholdService, UserException, InvalidArgException, HouseholdException, \
    get_the_ingredient_with_the_closest_expiration_date
from fastapi import APIRouter
from routers_boundaries.HouseholdBoundary import HouseholdBoundary, \
    HouseholdBoundaryWithGasPollution
from routers_boundaries.MealBoundary import meal_types
from routers_boundaries.InputsForApiCalls import (UserInputForAddUser, IngredientInput
, IngredientToRemoveByDateInput, ListIngredientsInput, UserInputForChanges, Date)
from routers_boundaries.UserBoundary import UserBoundary
from routers_boundaries.recipe_boundary import RecipeBoundaryWithGasPollution, RecipeBoundary

router = APIRouter(prefix='/usersAndHouseholdManagement',
                   tags=['users and household operations'])  ## tag is description of router
from datetime import date
import logging

recipes_service = RecipesService()

user_household_service = UsersHouseholdService()

logger = logging.getLogger("my_logger")


# Adding a new household with the user who created it
@router.post("/createNewHousehold")
async def createNewHousehold(user_mail: str, household_name: str, ingredients: Optional[ListIngredientsInput]):
    try:
        logger.info(f"Creating new household with ingredients : {ingredients.ingredients} and name : {household_name}")
        household_id = await user_household_service.create_household(user_mail, household_name)
        if ingredients is not None:
            await user_household_service.add_ingredients_to_household(user_mail, household_id, ingredients)
        logger.info(f"Household '{household_name}' added successfully by user '{user_mail}'")
        return {"message": "Household added successfully", 'household_id': household_id}
    except UserException as e:
        logger.error(f"Error creating household: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))
    except InvalidArgException as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


@router.delete("/deleteHousehold")
async def delete_household_by_id(household_id: str):
    try:
        logger.info(f"Try to delete household '{household_id}'")
        await user_household_service.delete_household(household_id)
        logger.info(f"Household deleted successfully")
    except HouseholdException as e:
        logger.error(f"Error deleting household: {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Adding a new user
@router.post("/addUser")
async def add_user(user: UserInputForAddUser):
    try:
        await user_household_service.create_user(user.first_name, user.last_name, user.email, user.country,
                                                 user.state)
        logger.info(f"User '{user.email}' added successfully")
        return {"message": f"Successfully Added User {user.email}"}
    except UserException as e:
        logger.error(f"Error creating user: {e.message}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.message))
    except InvalidArgException as e:
        logger.error(f"Error adding user: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


# Getting a user by email
@router.get("/getUser")
async def get_user(user_email: str):
    try:
        user = await user_household_service.get_user(user_email)
        logger.info(f"User '{user_email}' retrieved successfully")
        households: Dict[str, HouseholdBoundary] = {}
        for household_id in user.households:
            try:
                household = await user_household_service.get_household_user_by_id(user_email, household_id)
                if isinstance(household, HouseholdBoundary):
                    households[household_id] = household
            except HouseholdException:
                logger.error(f"Household {household_id} dose not exist")

        user.households = households
        return user
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, UserException) else status.HTTP_400_BAD_REQUEST,
            detail=str(e.message))


@router.put("/updatePersonalUserInfo")
async def update_personal_user_info(user: UserInputForChanges):
    try:
        await user_household_service.change_user_info(user.email, user.first_name, user.last_name, user.country,
                                                      user.state)
        logger.info(f"User '{user.email}' updated successfully")
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
            , detail=str(e.message))


@router.delete("/deleteUser")
async def delete_user(user_email: str):
    try:
        logger.info(f"Try to delete user '{user_email}'")
        await user_household_service.delete_user(user_email)
        logger.info(f"Deleted user '{user_email}'")
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Getting a household user by ID
@router.get("/getHouseholdUserById")
async def get_household_user_by_id(user_email: str, household_id: str):
    try:
        logger.info(f"Looking for user with '{user_email}' and '{household_id}'...")
        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        logger.info(f"Household '{household_id}' user retrieved successfully for user '{user_email}'")
        return household
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household user by ID: '{household_id}'")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, UserException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))


@router.get("/getHouseholdAndUsersDataById")
async def get_household_and_users_data_by_id(user_email: str, household_id: str):
    try:
        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            logger.info("convert HouseholdBoundary to HouseholdBoundaryWithUsersData")
            return await user_household_service.to_household_boundary_with_users_data(household)
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household user by ID: '{household_id}'")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, UserException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))


# Getting a household user by name
@router.get("/getHouseholdUserByName")
async def get_household_user_by_name(user_email: str, household_name: str):
    try:
        households = await user_household_service.get_household_user_by_name(user_email, household_name)
        logger.info(f"Household '{household_name}' users retrieved successfully for user '{user_email}'")
        return households
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving household users by name: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, UserException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))


@router.get("/getAllHouseholdsDetailsByUserMail")
async def get_all_household_details_by_user_mail(user_email: str):
    try:
        user = await user_household_service.get_user(user_email)
        households = []
        for _ in user.households:
            try:
                household_details = await user_household_service.get_household_user_by_id(user_email, _)
                households.append(household_details)
            except HouseholdException as e:
                logger.error(f"Error retrieving household details for user {user_email} and household id : {_}")
        return households
    except (UserException, InvalidArgException) as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if isinstance(e, UserException) else status.HTTP_400_BAD_REQUEST,
            detail=str(e.message))


# Adding a user to a household
@router.post("/addUserToHousehold")
async def add_user_to_household(user_email: str, household_id: str):
    try:
        await user_household_service.add_user_to_household(user_email, household_id)
        logger.info(f"User '{user_email}' added to household '{household_id}' successfully")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding user to household: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


@router.delete("/removeUserFromHousehold")
async def remove_user_from_household(user_email: str, household_id: str):
    try:
        await user_household_service.remove_user_from_household(user_email, household_id)
        logger.info(f"User '{user_email}' removed from household '{household_id}' successfully")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error remove user to household: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))


# Adding an ingredient to a household by name
@router.post("/addIngredientToHouseholdByIngredientName")
async def add_ingredient_to_household_by_ingredient_name(user_email: str, household_id: str,
                                                         ingredient: IngredientInput):
    logger.info(f"try to add ingredient: {ingredient.name} : {ingredient.amount} by name")
    try:
        await user_household_service.add_ingredient_to_household_by_ingredient_name(user_email, household_id,
                                                                                    ingredient.name,
                                                                                    ingredient.amount,
                                                                                    ingredient.unit)
        logger.info(
            f"Ingredient '{ingredient.name}' added to household '{household_id}' successfully by user "
            f"'{user_email}'")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding ingredient to household by name: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))
    except ValueError as e:
        logger.error(f"Ingredient {ingredient.name} dose not exist: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/updateIngredientInHousehold")
async def updateIngredientInHousehold(user_email: str, household_id: str,
                                      ingredient: IngredientToRemoveByDateInput):
    try:
        # Create a date object from the provided year, month, and day
        ingredient_date = date(ingredient.date.year, ingredient.date.month, ingredient.date.day)
        if ingredient_date > date.today():
            logger.error("Provided date is after than today")
            raise HTTPException(status_code=400, detail="Provided date cannot be earlier than today")
    except ValueError:
        logger.error("Invalid date provided")
        raise HTTPException(status_code=400, detail="Invalid date provided")

    try:
        await user_household_service.update_ingredient_by_date(user_email,
                                                               household_id,
                                                               ingredient.ingredient_data.name,
                                                               ingredient.ingredient_data.amount,
                                                               ingredient_date)
        logger.info(
            f"Ingredient '{ingredient.ingredient_data.name}' in {ingredient_date}"
            f"from household '{household_id}' update successfully by user '{user_email}'")
    except InvalidArgException as e:
        m = str(f"Error removing ingredient {ingredient.ingredient_data.name}"
                f" from household: {household_id} in date {ingredient_date}")
        logger.error(m)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(m))


# Adding a list of ingredients to a household
@router.post("/addListIngredientsToHousehold")
async def add_list_ingredients_to_household(user_email: str, household_id: str, list_ingredients: ListIngredientsInput):
    try:
        await user_household_service.add_ingredients_to_household(user_email, household_id, list_ingredients)
        logger.info(f"List of ingredients added to household '{household_id}' successfully by user '{user_email}'")
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error adding ingredient to household by name: {e.message}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))


'''
Remove ingredient from a certain date
'''


@router.delete("/removeIngredientFromHouseholdByDate")
async def remove_ingredient_from_household_by_date(user_email: str, household_id: str,
                                                   ingredient: IngredientToRemoveByDateInput):
    try:
        # Create a date object from the provided year, month, and day
        ingredient_date = date(ingredient.date.year, ingredient.date.month, ingredient.date.day)
    except ValueError:
        logger.error("Invalid date provided")
        raise HTTPException(status_code=400, detail="Invalid date provided")

    try:
        await user_household_service.remove_household_ingredient_by_date(user_email,
                                                                         household_id,
                                                                         ingredient.ingredient_data.name,
                                                                         ingredient.ingredient_data.amount,
                                                                         ingredient_date)
        logger.info(
            f"Ingredient '{ingredient.ingredient_data.name}' in {ingredient_date}"
            f" removed from household '{household_id}' successfully by user '{user_email}'")
    except InvalidArgException as e:
        m = str(f"Error removing ingredient {ingredient.ingredient_data.name}"
                f" from household: {household_id} in date {ingredient_date}")
        logger.error(m)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(m))


# Removing an ingredient from a household
@router.delete("/removeIngredientFromHousehold")
async def remove_ingredient_from_household(user_email: str, household_id: str, ingredient: IngredientInput):
    try:

        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            await user_household_service.remove_one_ingredient_from_household(household, ingredient.name,
                                                                              ingredient.amount,
                                                                              ingredient.ingredient_id)
        logger.info(
            f"Ingredient '{ingredient.name}' "
            f"removed {ingredient.amount} from household '{household_id}' successfully by user '{user_email}'")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))
    except InvalidArgException as e:
        logger.error(f"Error removing ingredient"
                     f" {ingredient.ingredient_id} : {ingredient.name} from household: {household_id} error : {e.message}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))


# Getting all ingredients in a household
@router.get("/getAllIngredientsInHousehold")
async def get_all_ingredients_in_household(user_email: str, household_id: str):
    try:
        ingredients = await user_household_service.get_all_ingredients_in_household(user_email, household_id)
        logger.info(f"All ingredients retrieved from household '{household_id}' successfully by user '{user_email}'")
        return ingredients
    except (UserException, InvalidArgException, HouseholdException) as e:
        logger.error(f"Error retrieving all ingredients from household: {e}")
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=str(e.message))


@router.post("/useRecipeByRecipeId")
async def use_recipe_by_recipe_id(users_email: List[str], household_id: str,
                                  meal: str, dishes_num: float, recipe_id: str):
    try:
        mealT = None
        for meal_type in meal_types:
            if meal_type == meal:
                mealT = meal_type
        if mealT is None:
            logger.error(f"No meal type")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail=f"Invalid meal meals type is : '{meal_types}'")
        if dishes_num <= 0:
            raise Exception(f"dishes num should be grater than 0")
        logger.info(f"Users {users_email} try using recipe {recipe_id} x {dishes_num} for household '{household_id}'")
        await user_household_service.use_recipe(users_email, household_id, recipe_id,
                                                mealT, dishes_num)
        logger.info(f"Successfully '{household_id}' using recipe '{recipe_id}' by users '{users_email}'")
    except (UserException, InvalidArgException, HouseholdException) as e:
        status_code = status.HTTP_400_BAD_REQUEST if isinstance(e, InvalidArgException) else status.HTTP_404_NOT_FOUND
        logger.error(f"Error retrieving : {e.message}")
        raise HTTPException(status_code=status_code, detail=str(e.message))
    except ValueError as e:
        logger.error(f"Error retrieving : {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving : {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/getMealTypes")
def get_meal_types():
    return [f'{meal_type}' for meal_type in meal_types]


from concurrent.futures import ThreadPoolExecutor


@router.get("/getAllRecipesThatHouseholdCanMake")
async def get_all_recipes_that_household_can_make(user_email: str, household_id: str,
                                                  co2_weight: Optional[float] = 0.5,
                                                  expiration_weight: Optional[float] = 0.5):
    try:
        recipes_rv: List[RecipeBoundaryWithGasPollution] = []
        household = await user_household_service.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            recipes = await recipes_service.get_recipes_by_ingredients_lst(household.get_all_unique_names_ingredient(),
                                                                           False)

            tasks = [user_household_service.check_if_household_can_make_the_recipe(household_id,
                                                                                   str(recipe.recipe_id),
                                                                                   0)
                     for recipe in recipes]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for recipe, result in zip(recipes, results):
                if isinstance(result, Exception):
                    logger.error(f"Exception occurred while checking recipe {recipe.recipe_id}: {result}")
                elif result:
                    recipes_rv.append(recipe)
        recipes = recipes_rv
        # # Calculate closest expiration date for each recipe
        if isinstance(household, HouseholdBoundaryWithGasPollution):
            with ThreadPoolExecutor() as executor:
                loop = asyncio.get_running_loop()
                expiration_tasks = [
                    loop.run_in_executor(executor, get_the_ingredient_with_the_closest_expiration_date, recipe,
                                         household.ingredients)
                    for recipe in recipes]
                expiration_results = await asyncio.gather(*expiration_tasks, return_exceptions=True)

            for recipe, closest_days_to_expire in zip(recipes, expiration_results):
                if isinstance(closest_days_to_expire, Exception):
                    logger.error(
                        f"Exception occurred while calculating expiration for recipe"
                        f" {recipe.recipe_id}: {closest_days_to_expire}")
                else:
                    recipe.set_closest_expiration_days(closest_days_to_expire)
        # Sort recipes by composite score with given weights
        recipes.sort(key=lambda r: r.composite_score(co2_weight, expiration_weight), reverse=True)
        return recipes
    except (Exception, TypeError, ValueError) as e:
        logger.error(f"Error retrieving recipes for household {household_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/checkIfHouseholdExistInSystem")
async def check_if_household_exist_in_system(household_id: str):
    try:
        await user_household_service.get_household_by_Id(household_id)
        logger.info(f"Household {household_id} exists in system")
        return True
    except HouseholdException as e:
        logger.error(f"Household {household_id} does not exist in system")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(f"Household {household_id} does not exist in system"))


@router.get("/checkIfHouseholdCanMakeRecipe")
async def check_if_household_can_make_recipe(household_id: str, recipe_id: str, dishes_num: Optional[float] = 1):
    return await user_household_service.check_if_household_can_make_the_recipe(household_id, recipe_id, dishes_num)


@router.post("/getGasPollutionOfHouseholdInRangeDates")
async def get_gas_pollution_of_household_in_range_dates(user_email: str, household_id: str, startDate: Date,
                                                        endDate: Date):
    try:
        # Create a date object from the provided year, month, and day
        start = date(startDate.year, startDate.month, startDate.day)
        end = date(endDate.year, endDate.month, endDate.day)
        # Check if the start date is before the end date
        if start >= end:
            logger.error(f"Start date {start} must be before end date {end}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date must be before end date")
        logger.info(f"Retrieve a gas pollution of household {household_id} in range time {start} - {end}")
        return await user_household_service.calculate_gas_pollution_of_household_in_range_dates(user_email,
                                                                                                household_id, start,
                                                                                                end)
    except ValueError:
        logger.error("Invalid date provided")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date provided")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.__dict__)


@router.post("/getGasPollutionOfUserInRangeDates")
async def get_gas_pollution_of_user_in_range_dates(user_email: str, startDate: Date, endDate: Date):
    try:
        # Create a date object from the provided year, month, and day
        start = date(startDate.year, startDate.month, startDate.day)
        end = date(endDate.year, endDate.month, endDate.day)
        # Check if the start date is before the end date
        if start >= end:
            logger.error(f"Start date {start} must be before end date {end}")
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        logger.info(f"Retrieve a gas pollution of user {user_email} in range time {start} - {end}")
        return await user_household_service.calculate_gas_pollution_of_user_in_range_dates(user_email, start, end)
    except ValueError:
        logger.error("Invalid date provided")
        raise HTTPException(status_code=400, detail="Invalid date provided")
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.__dict__)


from fastapi import File, UploadFile

# # Uploading an image for a household
# @router.post("/upload_user_image")
# async def upload_user_image(user_email: str, file: UploadFile = File(...)):
#     try:
#         split_tup = os.path.splitext(file.filename)
#         file_extension = split_tup[1]
#
#         image_url = await user_household_service.upload_file_to_storage(file,
#                                                                         f"images/users", user_email, file_extension)
#
#         # Log success
#         logger.info(f"Image uploaded for user '{user_email}' successfully")
#
#         # Return success response
#         return {"message": "Image uploaded successfully", "image_url": image_url}
#     except (UserException, InvalidArgException) as e:
#         logger.error(f"Unexpected error: {e.message}")
#         code = status.HTTP_404_NOT_FOUND if isinstance(e, UserException) else status.HTTP_400_BAD_REQUEST
#         raise HTTPException(status_code=code, detail=e.message)
#
#
# # from PIL import Image
# import base64
#
#
# @router.get("/get_user_images")
# async def get_user_images(file_path: str):
#     await user_household_service.download_file_from_storage(f"images/users/{file_path}", file_path)
#
#     rv = None
#     with open(file_path, "rb") as imageFile:
#         s = base64.b64encode(imageFile.read())
#         rv = str(bytearray(s))
#
#     os.remove(file_path)
#     return rv
