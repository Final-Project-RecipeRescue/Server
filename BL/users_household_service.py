import datetime
import logging
import os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import UploadFile
from BL.ingredient_service import IngredientService
from BL.recipes_service import RecipesService
from Data.HouseholdEntity import HouseholdEntity
from Data.MealEntity import MealEntity
from Data.UserEntity import UserEntity
from routers_boundaries.HouseholdBoundary import HouseholdBoundary, HouseholdBoundaryWithUsersData
import uuid
from DAL.firebase_db_connection import FirebaseDbConnection
from routers_boundaries.IngredientBoundary import IngredientBoundary, IngredientBoundaryWithExpirationData
from routers_boundaries.InputsForApiCalls import ListIngredientsInput
from routers_boundaries.MealBoundary import MealBoundary
from routers_boundaries.MealBoundary import meal_types
from routers_boundaries.UserBoundary import UserBoundary
import routers_boundaries.UserBoundary as user_entity_py
from Data.IngredientEntity import IngredientEntity
from routers_boundaries.recipe_boundary import RecipeBoundary

logger = logging.getLogger("my_logger")


def encoded_email(email: str) -> str:
    return email.replace('.', ',')


def decoded_email(email: str) -> str:
    return email.replace(',', '.')


ingredientService = IngredientService()

date_format = "%Y-%m-%d"


def to_ingredient_entity(ingredient: IngredientBoundary) -> IngredientEntity:
    ingredient_entity = IngredientEntity({})
    ingredient_entity.id = ingredient.ingredient_id
    ingredient_entity.name = ingredient.name
    ingredient_entity.purchase_date = ingredient.purchase_date
    ingredient_entity.amount = ingredient.amount
    ingredient_entity.unit = ingredient.unit
    return ingredient_entity


def to_ingredient_boundary(ingredient: object) -> IngredientBoundary:
    ingredientEntity = IngredientEntity(ingredient)
    return IngredientBoundary(
        ingredientEntity.id,
        ingredientEntity.name,
        ingredientEntity.amount,
        ingredientEntity.unit,
        datetime.strptime(ingredientEntity.purchase_date, date_format)
    )


def calc_expiration(ingredient: IngredientBoundary) -> Optional[datetime.date]:
    """Try to get by id"""
    ing_data = ingredientService.get_ingredient_by_id(int(ingredient.ingredient_id))
    if ing_data is None:
        '''Try to get by name'''
        ing_data = ingredientService.search_ingredient_by_name(ingredient.name)
        if ing_data is None:
            '''Try to find same ingredient by name'''
            ingredients_data = ingredientService.autocomplete_by_ingredient_name(ingredient.name)
            if ingredients_data is None:
                return None
            else:
                ing_data = ingredients_data[0]
                for ing in ingredients_data:
                    if ing.name.lower() == ingredient.name.lower():
                        ing_data = ing
    if ingredient.purchase_date is not None:
        date = datetime.strptime(ingredient.purchase_date, date_format)
        delta = timedelta(days=ing_data.expirationData)
        new_date = date + delta
        return new_date


def to_ingredient_boundary_with_expiration_data(ingredient: IngredientBoundary) -> IngredientBoundaryWithExpirationData:
    return IngredientBoundaryWithExpirationData(
        ingredient,
        calc_expiration(ingredient)
    )


def to_boundary_meal(meal: object):
    mealEntity = MealEntity(meal)
    return MealBoundary(
        mealEntity.users,
        mealEntity.number_of_dishes
    )


def to_meal_entity(meal: MealBoundary) -> MealEntity:
    meal_entity = MealEntity({})
    meal_entity.users = [user for user in meal.users]
    meal_entity.number_of_dishes = meal.number_of_dishes
    return meal_entity


def to_user_boundary(user_data: object) -> UserBoundary:
    user_entity = UserEntity(user_data)
    first_name = user_entity.first_name
    last_name = user_entity.last_name
    email = user_entity.user_email
    country = user_entity.country
    state = user_entity.state
    image = user_entity.image
    households = []
    meals = {}
    for household in user_entity.households:
        if household:
            households.append(household)
    for date, mealsTypes in user_entity.meals.items():
        meals[date] = {}
        for type, recipe_ids in mealsTypes.items():
            meals[date][type] = {}
            for recipe_id, meal in recipe_ids.items():
                meals[date][type][recipe_id] = to_boundary_meal(meal)

    return UserBoundary(first_name, last_name, email, image, households, meals, country, state)


def to_user_entity(user: UserBoundary) -> UserEntity:
    user_entity = UserEntity({})
    user_entity.user_email = user.user_email
    user_entity.first_name = user.first_name
    user_entity.last_name = user.last_name
    user_entity.country = user.country
    user_entity.state = user.state
    user_entity.image = user.image
    user_entity.households = user.households
    user_entity.meals = {}
    for date, mealsTypes in user.meals.items():
        user_entity.meals[date] = {}
        for type, recipe_ids in mealsTypes.items():
            user_entity.meals[date][type] = {}
            for recipe_id, meal in recipe_ids.items():
                user_entity.meals[date][type][recipe_id] = to_meal_entity(meal).__dict__
    return user_entity


def to_household_boundary(household_data: object) -> HouseholdBoundary:
    household_entity = HouseholdEntity(household_data)
    household_id = household_entity.id
    household_name = household_entity.name
    household_image = household_entity.image
    household_participants = household_entity.participants
    household_ingredients = {}
    for ingredient_id, dates in household_entity.ingredients.items():
        household_ingredients[ingredient_id] = []
        for date, ingredient_entity in dates.items():
            ingredient_boundary = to_ingredient_boundary_with_expiration_data(to_ingredient_boundary(ingredient_entity))
            household_ingredients[ingredient_id].append(ingredient_boundary)

    household_meals = {}
    for date, mealsTypes in household_entity.meals.items():
        household_meals[date] = {}
        for type, recipe_ids in mealsTypes.items():
            household_meals[date][type] = {}
            for recipe_id, meals in recipe_ids.items():
                household_meals[date][type][recipe_id] = []
                for meal_entity in meals:
                    meal_boundary = to_boundary_meal(meal_entity)
                    household_meals[date][type][recipe_id].append(meal_boundary)

    return HouseholdBoundary(household_id,
                             household_name,
                             household_image,
                             household_participants,
                             household_ingredients,
                             household_meals)


def to_household_entity(household: HouseholdBoundary) -> HouseholdEntity:
    household_entity = HouseholdEntity({})
    household_entity.id = household.household_id
    household_entity.name = household.household_name
    household_entity.image = household.household_image
    household_entity.participants = household.participants
    household_entity.ingredients = {}
    for ingredient_id, ingredients_lst in household.ingredients.items():
        household_entity.ingredients[ingredient_id] = {}
        ingredient_id_dict = household_entity.ingredients[ingredient_id]
        for ingredient in ingredients_lst:
            ingredient_id_dict[ingredient.purchase_date] = to_ingredient_entity(ingredient).__dict__
    household_entity.meals = {}
    for date, mealTypes in household.meals.items():
        household_entity.meals[date] = {}
        date_dict = household_entity.meals[date]
        for type, recipe_ids in mealTypes.items():
            date_dict[type] = {}
            type_meal_dict = date_dict[type]
            for recipe_id, meals in recipe_ids.items():
                type_meal_dict[recipe_id] = []
                recipe_meal_lst = type_meal_dict[recipe_id]
                for meal in meals:
                    recipe_meal_lst.append(to_meal_entity(meal).__dict__)
    return household_entity


def add_meal_to_user(user: UserBoundary, new_meal: MealBoundary, date: str, mealType: meal_types,
                     recipe_id: str):
    if not user.meals:
        user.meals = {}
    try:
        date_meals = user.meals[date]
        try:
            type_meals = date_meals[mealType]
            try:
                meal = type_meals[recipe_id]
                meal.number_of_dishes += new_meal.number_of_dishes
            except KeyError:
                type_meals[recipe_id] = new_meal
        except KeyError:
            date_meals[mealType] = {recipe_id: new_meal}
    except KeyError:
        user.meals[date] = {mealType: {recipe_id: new_meal}}


def add_meal_to_household(household: HouseholdBoundary, new_meal: MealBoundary, date: str, mealType: meal_types,
                          recipe_id: str):
    if not household.meals:
        household.meals = {}
    try:
        date_meals = household.meals[date]
        try:
            type_meals = date_meals[mealType]
            try:
                meals_with_same_recipe_id = type_meals[recipe_id]
                meals_with_same_recipe_id.append(new_meal)
            except KeyError:
                type_meals[recipe_id] = [new_meal]
        except KeyError:
            date_meals[mealType] = {recipe_id: [new_meal]}
    except KeyError:
        household.meals[date] = {mealType: {recipe_id: [new_meal]}}


class UsersHouseholdService:
    def __init__(self):
        self.firebase_instance = FirebaseDbConnection.get_instance()
        self.recipes_service = RecipesService()

    def check_email(self, email: str):
        if not user_entity_py.is_valid_email(email):
            raise InvalidArgException("Invalid email format")

    async def check_user_if_user_exist(self, email: str):
        if self.firebase_instance.get_firebase_data(f'users/{encoded_email(email)}') == None:
            raise UserException("User not exists")

    # TODO:need to add option to enter image
    async def create_household(self, user_mail: str, household_name: str) -> str:
        try:
            self.check_email(user_mail)
        except InvalidArgException as e:
            raise InvalidArgException("Invalid email format")
        await self.check_user_if_user_exist(user_mail)
        user_data = self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}')

        household_id = str(uuid.uuid4())
        while (self.firebase_instance.get_firebase_data(f'households/{household_id}') != None):
            household_id = str(uuid.uuid4())
        user = to_user_boundary(user_data)
        household = HouseholdBoundary(household_id,
                                      household_name,
                                      None,
                                      [user.user_email],
                                      {},
                                      {})
        self.firebase_instance.write_firebase_data(f'households/{household_id}',
                                                   to_household_entity(household).__dict__)
        user.households.append(household_id)
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_mail)}', to_user_entity(user).__dict__)
        return household_id

    # TODO:need to add option to enter image
    async def create_user(self, user_first_name: str, user_last_name: str, user_mail: str, country: str,
                          state: Optional[str]):
        self.check_email(user_mail)
        if self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}') != None:
            raise UserException("User already exists")
        if user_first_name == "" or user_last_name == "" or country == "":
            raise InvalidArgException("Fill all fields before")
        user = UserBoundary(user_first_name,
                            user_last_name,
                            user_mail,
                            None,
                            [],
                            {},
                            country,
                            state)
        self.firebase_instance.write_firebase_data(f'users/{encoded_email(user_mail)}', to_user_entity(user).__dict__)

    async def get_user(self, email: str) -> UserBoundary:
        self.check_email(email)
        e_email = encoded_email(email)
        user = self.firebase_instance.get_firebase_data(f'users/{e_email}')
        if not user:
            raise UserException("User does not exist")
        user_boundary = to_user_boundary(user)
        return user_boundary

    async def change_user_info(self, user_email: str, first_name: Optional[str], last_name: Optional[str],
                               country: Optional[str], state: Optional[str]):
        self.check_email(user_email)
        user = await self.get_user(user_email)
        if not user:
            raise UserException("User does not exist")
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if country is not None:
            user.country = country
        if state is not None:
            user.state = state
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}', to_user_entity(user).__dict__)

    async def get_household_user_by_id(self, user_email: str, household_id: str) -> HouseholdBoundary:
        user = await self.get_user(user_email)
        household = await self.get_household_by_Id(household_id)
        if not household:
            raise HouseholdException("Household does not exist")
        if household_id in user.households and user_email in household.participants:
            return household
        raise HouseholdException(f"This user : {user_email} does not have access to this household : {household_id}")

    async def get_household_user_by_name(self, user_email, household_name) -> List[HouseholdBoundary]:
        user_entity = await self.get_user(user_email)
        households = []
        for id in user_entity.households:
            household = await self.get_household_user_by_id(user_email, id)
            if not household:
                raise HouseholdException(
                    "You have a problem in the DB with the user the household is found but with the collection of households it is not found")
            if household.household_name == household_name:
                households.append(household)
        if households.__len__() == 0:
            raise HouseholdException("Household does not exist")
        return households

    async def get_household_by_Id(self, household_id: str) -> HouseholdBoundary:
        household = self.firebase_instance.get_firebase_data(f'households/{household_id}')
        if not household:
            raise HouseholdException('Household does not exist')
        return to_household_boundary(household)

    async def add_user_to_household(self, user_email: str, household_id: str):
        user_boundary = await self.get_user(user_email)
        household = await self.get_household_by_Id(household_id)
        if isinstance(household, HouseholdBoundary):
            for user in household.participants:
                if user == user_boundary.user_email:
                    raise HouseholdException('User already exists in the household')
            household.participants.append(user_email)
            user_boundary.households.append(household.household_id)

            self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                        to_household_entity(household).__dict__)
            self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                        to_user_entity(user_boundary).__dict__)

    async def remove_user_from_household(self, user_email, household_id):
        user_boundary = await self.get_user(user_email)
        household = await self.get_household_by_Id(household_id)
        if isinstance(household, HouseholdBoundary):
            if user_email in household.participants and household_id in user_boundary.households:
                household.participants.remove(user_email)
                user_boundary.households.remove(household_id)
                self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                            to_household_entity(household).__dict__)
                self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                            to_user_entity(user_boundary).__dict__)
            else:
                raise Exception('User not exists in the household')

    async def add_ingredient_to_household_by_ingredient_name(self, user_email: str, household_id: str,
                                                             ingredient_name: str,
                                                             ingredient_amount: float):
        if ingredient_amount <= 0:
            raise InvalidArgException(f"Ingredient amount need to be grater then 0")
        household = await self.get_household_user_by_id(user_email, household_id)
        ingredient_data = ingredientService.search_ingredient_by_name(ingredient_name)
        if ingredient_data is None:
            raise ValueError(f"Ingredient {ingredient_name} Not Found")
        new_ingredient = IngredientBoundary(ingredient_data.ingredient_id, ingredient_data.name, ingredient_amount,
                                            "gram",
                                            datetime.now())
        try:
            existing_ingredients = household.ingredients[str(new_ingredient.ingredient_id)]
            found = False
            for ing in existing_ingredients:
                if ing.purchase_date == new_ingredient.purchase_date:
                    ing.amount += ingredient_amount
                    found = True
                    break
            if not found:
                existing_ingredients.append(new_ingredient)
            household.ingredients[new_ingredient.ingredient_id] = existing_ingredients
        except KeyError as e:
            logger.info(f"Household {household.household_name}"
                        f" with id {household.household_id} add new ingredient {new_ingredient.ingredient_id} "
                        f"with name {ingredient_name}")
            household.ingredients[new_ingredient.ingredient_id] = [new_ingredient]

        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)
    async def add_ingredients_to_household(self, user_email: str, household_id: str,ingredients_lst_names_and_amounts : ListIngredientsInput ):
        household = await self.get_household_user_by_id(user_email, household_id)
        for ingredient in ingredients_lst_names_and_amounts.ingredients:
            if ingredient.amount <= 0:
                logger.error(f"Ingredient {ingredient.name} amount need to be grater then 0")
            ingredient_data = ingredientService.search_ingredient_by_name(ingredient.name)
            if ingredient_data is None:
                logger.error(f"Ingredient {ingredient.name} Not Found")
            new_ingredient = IngredientBoundary(ingredient_data.ingredient_id, ingredient_data.name, ingredient.amount,
                                                "gram",
                                                datetime.now())
            try:
                existing_ingredients = household.ingredients[str(new_ingredient.ingredient_id)]
                found = False
                for ing in existing_ingredients:
                    if ing.purchase_date == new_ingredient.purchase_date:
                        ing.amount += ingredient.amount
                        found = True
                        break
                if not found:
                    existing_ingredients.append(new_ingredient)
                household.ingredients[new_ingredient.ingredient_id] = existing_ingredients
            except KeyError as e:
                logger.info(f"Household {household.household_name}"
                            f" with id {household.household_id} add new ingredient {new_ingredient.ingredient_id} "
                            f"with name {ingredient_data.name}")
                household.ingredients[new_ingredient.ingredient_id] = [new_ingredient]

        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)
    async def remove_household_ingredient_by_date(self, user_mail: str, household_id, ingredient_name: str,
                                                  ingredient_amount: float, ingredient_date: datetime.date):
        if ingredient_amount <= 0:
            raise InvalidArgException(f"Ingredient amount need to be greater than 0")
        household = await self.get_household_user_by_id(user_mail, household_id)
        ingredient_name = ingredient_name[0].upper() + ingredient_name[1:].lower()
        ingredient_data = ingredientService.search_ingredient_by_name(
            ingredient_name)  # ingredientsCRUD.search_ingredient(ingredient_name)
        if not ingredient_data:
            raise InvalidArgException(f"The ingredient {ingredient_name} dose not exist in the system")
        ing_id = ingredient_data.ingredient_id
        try:
            for ing in household.ingredients[ing_id]:
                if isinstance(ing, IngredientBoundary):
                    if ing.purchase_date == ingredient_date.strftime(date_format):
                        if ingredient_amount > ing.amount:
                            raise InvalidArgException(
                                f"The amount you wanted to remove from the household {household.household_name}"
                                f" is greater than the amount that is in ingredient {ingredient_name} on this date. "
                                f"The maximum amount is {ing.amount}")
                        if ing.amount >= ingredient_amount:
                            ing.amount -= ingredient_amount
                        if ing.amount <= 0:
                            household.ingredients[ing_id].remove(ing)
                        self.firebase_instance.update_firebase_data(f'households/{household_id}'
                                                                    , to_household_entity(household).__dict__)
                        return
            raise InvalidArgException(
                f"No such ingredient '{ingredient_name}' in household '{household.household_name}' with date "
                f"{ingredient_date.strftime(date_format)}")
        except KeyError as e:
            raise InvalidArgException(f"No such ingredient {ingredient_name} in household {household.household_name}")

    async def remove_household_ingredient(self, user_mail: str, household_id, ingredient_name: str,
                                          ingredient_amount: float, ingredient_id: Optional[str]):
        if ingredient_amount < 0:
            raise InvalidArgException("Invalid ingredient amount, it cannot be a negative number")

        household = await self.get_household_user_by_id(user_mail, household_id)
        if ingredient_id is None:
            ingredient_name = ingredient_name.capitalize()  # Convert to title case
            ingredient_data = ingredientService.search_ingredient_by_name(
                ingredient_name)  # self.ingredientsCRUD.search_ingredient(ingredient_name)
            ing_id = str(ingredient_data.ingredient_id)
        else:
            ing_id = str(ingredient_id)
        if ing_id not in household.ingredients.keys():
            ing_id = None
            ingredients_data = ingredientService.autocomplete_by_ingredient_name(ingredient_name)
            for ing in ingredients_data:
                if ing.ingredient_id in household.ingredients.keys():
                    ingredients_data = ing
                    ing_id = str(ingredient_data.ingredient_id)
            if ing_id is None:
                raise InvalidArgException(f"'{ingredient_name}' not found in household ingredients")

        ingredient_lst = household.ingredients[ing_id]
        ingredient_lst.sort(key=lambda x: x.purchase_date)
        sum_amounts = sum([ing.amount for ing in ingredient_lst])

        if sum_amounts < ingredient_amount:
            raise InvalidArgException(
                f"The max amount to remove of ingredient '{ingredient_name}' with id : {ing_id} is {sum_amounts} you try remove {ingredient_amount}")

        remaining_amount = ingredient_amount
        updated_ingredients = []

        for ing in ingredient_lst:
            if ing.amount <= remaining_amount:
                remaining_amount -= ing.amount
                ing.amount = 0
            else:
                ing.amount -= remaining_amount
                remaining_amount = 0
            if ing.amount > 0:
                updated_ingredients.append(ing)

        household.ingredients[ing_id] = updated_ingredients
        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)

    async def get_all_ingredients_in_household(self, user_email, household_id) -> dict:
        household = await self.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            for ingredient_id, data in household.ingredients.items():
                household.ingredients[ingredient_id].sort(key=lambda x: x.purchase_date)
            return household.ingredients

    def get_sum_of_ing_in_household_byID(self, ingredient: IngredientBoundary, household: HouseholdBoundary):
        return sum(
            ing.amount for ing in household.ingredients[str(ingredient.ingredient_id)])

    async def check_ingredient_availability(self, household: HouseholdBoundary,
                                            recipe_ingredient: IngredientBoundary,
                                            dishes_number: float) -> bool:
        global logger_message
        try:
            '''Try to check if ingredient is availability by ID'''
            sum_amount = self.get_sum_of_ing_in_household_byID(recipe_ingredient, household)
            logger_message = str(f"Household {household.household_id} dont hava enough {recipe_ingredient.name} :"
                                 f" {recipe_ingredient.ingredient_id}."
                                 f" The household have {sum_amount} and needed {recipe_ingredient.amount * dishes_number}")
            if sum_amount < recipe_ingredient.amount * dishes_number:
                logger.info(logger_message)
                return False
            return True
        except KeyError as e:
            '''Try to check if ingredient is availability by Name'''
            ing_data = ingredientService.search_ingredient_by_name(recipe_ingredient.name)
            if ing_data is None:
                logger.error(f"Ingredient {recipe_ingredient.name} not exist in system")
                return True
            id = ing_data.ingredient_id
            if id != recipe_ingredient.ingredient_id:
                recipe_ingredient.ingredient_id = id  ##Change ingredient ID for removing ingredient
                try:
                    sum_amount = self.get_sum_of_ing_in_household_byID(recipe_ingredient, household)
                    if sum_amount < recipe_ingredient.amount * dishes_number:
                        logger.info(logger_message)
                        return False
                    return True
                except KeyError as e:
                    '''Try to check if ingredient is availability by SubString'''
                    try:
                        unique_names = []
                        for ing_id, ing_s in household.ingredients.items():
                            unique_names += list(set([ing.name for ing in ing_s]))
                        for u_ing_name in unique_names:
                            if recipe_ingredient.name in u_ing_name or u_ing_name in recipe_ingredient.name:
                                logger.info(
                                    f"Captured by substring ing1 : {recipe_ingredient.name} ing2 : {u_ing_name}")
                                recipe_ingredient.name = u_ing_name
                                '''Change ingredient ID for removing ingredient'''
                                recipe_ingredient.ingredient_id = (
                                    ingredientService.search_ingredient_by_name(u_ing_name).ingredient_id)
                                break
                        sum_amount = self.get_sum_of_ing_in_household_byID(recipe_ingredient, household)
                        if sum_amount < recipe_ingredient.amount * dishes_number:
                            logger.info(logger_message)
                            return False
                        return True
                    except Exception:
                        logger.error(
                            f"Ingredient {recipe_ingredient.ingredient_id} :"
                            f" {recipe_ingredient.name} is not available in "
                            f"the household")
                        return False
            return False

    async def use_recipe(self, user_email: str, household_id: str, recipe_id: str,
                         mealType: meal_types, dishes_number: float):
        """Get household and recipe from DB"""
        household = await self.get_household_user_by_id(user_email, household_id)
        recipe = await self.recipes_service.get_recipe_by_id(recipe_id)
        """Check if everything exist"""
        if isinstance(household, HouseholdBoundary) and isinstance(recipe, RecipeBoundary):
            ing_to_remove : [IngredientBoundary]= []
            logger.info(f"recipe {recipe_id} ingredients : {[ing.name for ing in recipe.ingredients]}")
            for ingredient in recipe.ingredients:
                if not await self.check_ingredient_availability(household, ingredient, dishes_number):
                    message = (f"Household '{household.household_name}' id : '{household.household_id}'"
                               f" does not have enough '{ingredient.name}' : '{ingredient.ingredient_id}' ingredient for"
                               f" recipe '{recipe_id}'. Needed: {ingredient.amount * dishes_number}")
                    try:
                        s = sum(ingredient.amount for ingredient in household.ingredients[ingredient.ingredient_id])
                        message += f"Available: {s}"
                    except KeyError as e:
                        pass

                    logger.error(message)
                    raise InvalidArgException(message)

            '''There is enough of all the ingredients to use in the recipe'''
            '''Removing the ingredients in a household'''
            for recipe_ingredient in recipe.ingredients:
                await self.remove_household_ingredient(user_email, household_id, recipe_ingredient.name,
                                                       recipe_ingredient.amount * dishes_number,
                                                       recipe_ingredient.ingredient_id)
            household = await self.get_household_user_by_id(user_email, household_id)
            new_meal = MealBoundary([user_email], dishes_number)
            add_meal_to_household(household, new_meal, datetime.now().strftime("%Y-%m-%d"), mealType, recipe_id)
            user = await self.get_user(user_email)
            add_meal_to_user(user, new_meal, datetime.now().strftime("%Y-%m-%d"), mealType, recipe_id)
            self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                        to_user_entity(user).__dict__)

            self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                        to_household_entity(household).__dict__)
        else:
            raise InvalidArgException(f"The household id or recipe id is invalid")

    async def check_if_household_can_make_the_recipe(self, household_id: str, recipe_id: str,
                                                     dishes_number: int) -> bool:
        household = await self.get_household_by_Id(household_id)
        recipe = await self.recipes_service.get_recipe_by_id(recipe_id)
        if isinstance(household, HouseholdBoundary) and isinstance(recipe, RecipeBoundary):
            for ingredient in recipe.ingredients:
                if not await self.check_ingredient_availability(household, ingredient, dishes_number):
                    return False
            return True
        return False

    async def delete_user(self, user_email):
        user = await self.get_user(user_email)
        if isinstance(user, UserBoundary):
            for household_id in user.households:
                household = await self.get_household_user_by_id(user_email, household_id)
                if isinstance(household, HouseholdBoundary):
                    household.participants.remove(user.user_email)
                    self.firebase_instance.update_firebase_data(f'households/{household_id}'
                                                                , to_household_entity(household).__dict__)
            self.firebase_instance.delete_firebase_data(f'users/{encoded_email(user_email)}')

    async def delete_household(self, household_id: str):
        household = await self.get_household_by_Id(household_id)
        if household is None:
            raise HouseholdException("No such household")
        if isinstance(household, HouseholdBoundary):
            for user_email in household.participants:
                user = await self.get_user(user_email)
                user.households.remove(household_id)
                self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                            to_user_entity(user).__dict__)
            self.firebase_instance.delete_firebase_data(f'households/{household_id}')

    async def upload_file_to_storage(self, file: UploadFile,
                                     storage_path: str, user_email: str, file_extension: str) -> str:
        user = await self.get_user(user_email)
        if not isinstance(user, UserBoundary):
            raise UserException("User dose not exist in system")

        user.image = f"{str(uuid.uuid4())}{file_extension}"
        temp_file_path = user.image

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        self.firebase_instance.upload_file(temp_file_path, storage_path)
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                    to_user_entity(user).__dict__)
        os.remove(temp_file_path)
        return f"{storage_path}/{temp_file_path}"

    # TODO:Fix return image
    async def download_file_from_storage(self, storage_path: str, local_file_path: str) -> str:
        self.firebase_instance.download_file(local_file_path, storage_path)

    async def to_household_boundary_with_users_data(self,
                                                    household: HouseholdBoundary) -> HouseholdBoundaryWithUsersData:
        users = []
        for user_email in household.participants:
            users.append(await self.get_user(user_email))
        return HouseholdBoundaryWithUsersData(household, users)


class HouseholdException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class UserException(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message


class InvalidArgException(ValueError):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
