import datetime
import logging
from datetime import datetime
from typing import List, Optional
from Data.HouseholdEntity import HouseholdEntity
from Data.MealEntity import MealEntityWithIngredients
from Data.UserEntity import UserEntity
from routers_boundaries.HouseholdBoundary import HouseholdBoundary
import uuid
from DAL.firebase_db_connection import FirebaseDbConnection
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.MealBoundary import MealBoundary, MealBoundaryWithIngredients, Ing
from routers_boundaries.MealBoundary import meal_types
from routers_boundaries.UserBoundary import UserBoundary
import routers_boundaries.UserBoundary as user_entity_py
from Data.IngredientEntity import IngredientEntity
from DAL.IngredientsCRUD import IngredientsCRUD
from BL.recipes_service import RecipesService

logger = logging.getLogger("my_logger")


def encoded_email(email: str) -> str:
    return email.replace('.', ',')


def decoded_email(email: str) -> str:
    return email.replace(',', '.')


date_format = "%Y-%m-%d"


def to_ingredient_boundary(ingredient: object) -> IngredientBoundary:
    try:
        return IngredientBoundary(
            int(ingredient['id']),
            ingredient['name'],
            float(ingredient['amount']),
            ingredient['unit'],
            datetime.strptime(ingredient['purchase_date'], date_format))
    except KeyError:
        return None


def to_boundary_meal(meal: object):
    mealEntity = MealEntityWithIngredients(meal)
    return MealBoundaryWithIngredients(
        datetime.strptime(mealEntity.used_date, date_format).date() if mealEntity.used_date is not None else None,
        mealEntity.type,
        mealEntity.users,
        mealEntity.recipe_id,
        float(mealEntity.number_of_dishes),
        mealEntity.ingredients)


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
    for date, meals_day in user_entity.meals.items():
        for meal in meals_day:
            meal['used_date'] = date
            meal_boundary = to_boundary_meal(meal)
            meal_boundary.users = [email]
            try:
                meals[date].append(meal_boundary)
            except KeyError:
                meals[date] = [meal_boundary]

    return UserBoundary(first_name, last_name, email, image, households, meals, country, state)


def to_household_boundary(household_data: object) -> HouseholdBoundary:
    household_id = household_data['id']
    household_name = household_data['name']
    household_image = None
    try:
        household_image = household_data['image']
    except KeyError:
        pass
    participants = household_data['participants']
    ingredients = {}
    try:
        for ingredient_name, ingredient_data in household_data['ingredients'].items():
            temp_lst = []
            for ingredient_date, data in ingredient_data.items():
                temp_lst.append(to_ingredient_boundary(data))
            if temp_lst.__len__() > 0:
                ingredients[f'{ingredient_name}'] = temp_lst
    except KeyError:
        pass
    meals = {}
    try:
        for date, meal_types in household_data['meals'].items():
            for type, recipe_ids in meal_types.items():
                for recipe_id, data in recipe_ids.items():
                    meal = MealBoundary(datetime.strptime(
                        f'{date}',
                        date_format),
                        type,
                        data['users'],
                        recipe_id,
                        data['number of dishes'])
                    try:
                        dates = meals[date]
                        try:
                            types = dates[type]
                            try:
                                types[recipe_id] = meal
                            except KeyError as e:
                                meals[date][type] = {recipe_id: meal}
                        except KeyError as e:
                            meals[date] = {type: {recipe_id: meal}}
                    except KeyError as e:
                        meals = {date: {type: {recipe_id: meal}}}
    except KeyError:
        pass
    return HouseholdBoundary(household_id, household_name, household_image, participants, ingredients, meals)


def to_ingredient_entity(ingredient: IngredientBoundary) -> IngredientEntity:
    return IngredientEntity(
        ingredient.ingredient_id,
        ingredient.name,
        ingredient.amount,
        ingredient.unit,
        ingredient.purchase_date)


def to_household_entity(household: HouseholdBoundary) -> HouseholdEntity:
    ingredients = {}
    if household.ingredients:
        for ingredient_name, ingredient_lst in household.ingredients.items():
            temp_dict = {}
            for ingredient in ingredient_lst:
                temp_dict[ingredient.purchase_date] = to_ingredient_entity(ingredient).__dict__
            if ingredient_lst.__len__() > 0:
                ingredients[ingredient_lst[0].name] = temp_dict
    meals = {}
    if household.meals:
        for date, meal_types in household.meals.items():
            for type, meal_recipe_ids in meal_types.items():
                for recipe_id, meal in meal_recipe_ids.items():
                    try:
                        dates = meals[date]
                        try:
                            types = dates[type]
                            try:
                                meal = types[recipe_id]
                                meals[date][type][recipe_id]['users'] = meal.users
                                meals[date][type][recipe_id]['number of dishes'] = meal.number_of_dishes
                            except KeyError as e:
                                meals[date][type] = {recipe_id: {
                                    'users': meal.users,
                                    'number of dishes': meal.number_of_dishes}}
                        except KeyError as e:
                            meals[date] = {type: {recipe_id: {
                                'users': meal.users,
                                'number of dishes': meal.number_of_dishes}}}
                    except KeyError as e:
                        meals = {date: {type: {recipe_id: {
                            'users': meal.users,
                            'number of dishes': meal.number_of_dishes}}}}

    return HouseholdEntity(
        household.household_id,
        household.household_name,
        household.household_image,
        household.participants,
        ingredients,
        meals)


def to_user_entity(user: UserBoundary) -> UserEntity:
    return UserEntity(user.__dict__)


class UsersHouseholdService:
    def __init__(self):
        self.firebase_instance = FirebaseDbConnection.get_instance()
        self.recipes_service = RecipesService()
        self.ingredientsCRUD = IngredientsCRUD()

    def check_email(self, email: str):
        if not user_entity_py.is_valid_email(email):
            raise InvalidArgException("Invalid email format")

    async def check_user_if_user_exist(self, email: str):
        if self.firebase_instance.get_firebase_data(f'users/{encoded_email(email)}') == None:
            raise UserException("User not exists")

    # TODO:need to add option to enter image
    async def create_household(self, user_mail: str, household_name: str) -> str:
        self.check_email(user_mail)
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

        if user.households is not None:
            user.households.append(household_id)
        else:
            user.households = [household_id]
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_mail)}', to_user_entity(user).__dict__)
        return household_id

    # TODO:need to add option to enter image
    async def create_user(self, user_first_name: str, user_last_name: str, user_mail: str, country: str, state: Optional[str]):
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

    async def get_household_user_by_id(self, user_email: str, household_id: str) -> HouseholdBoundary:
        user = await self.get_user(user_email)
        for id in user.households:
            if id == household_id:
                household_entity = self.firebase_instance.get_firebase_data(f'households/{id}')
                if not household_entity:
                    raise HouseholdException("Household does not exist")
                household_boundary = to_household_boundary(household_entity)
                return household_boundary
        raise HouseholdException("Household does not exist")

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
        household = to_household_boundary(household)
        return household

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

    async def add_ingredient_to_household_by_ingredient_name(self, user_email: str, household_id: str,
                                                             ingredient_name: str,
                                                             ingredient_amount: float):
        household = await self.get_household_user_by_id(user_email, household_id)
        ingredient_name = ingredient_name[0].upper() + ingredient_name[1:].lower()
        ingredient_data = self.ingredientsCRUD.search_ingredient(ingredient_name)
        if ingredient_data is None:
            raise ValueError(f"Ingredient {ingredient_name} Not Found")
        new_ingredient = IngredientBoundary(ingredient_data['id'], ingredient_data['name'], ingredient_amount, "",
                                            datetime.now())
        try:
            existing_ingredients = household.ingredients[ingredient_name]
            found = False
            for ing in existing_ingredients:
                if ing.purchase_date == new_ingredient.purchase_date:
                    ing.amount += ingredient_amount
                    found = True
                    break
            if not found:
                existing_ingredients.append(new_ingredient)
            household.ingredients[new_ingredient.name] = existing_ingredients
        except KeyError as e:
            household.ingredients[new_ingredient.name] = [new_ingredient]

        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)

    async def remove_household_ingredient_by_date(self, user_mail: str, household_id, ingredient_name: str,
                                                  ingredient_amount: float, ingredient_date: datetime.date):
        household = await self.get_household_user_by_id(user_mail, household_id)
        ingredient_name = ingredient_name[0].upper() + ingredient_name[1:].lower()
        try:
            for ing in household.ingredients[ingredient_name]:
                if isinstance(ing, IngredientBoundary):
                    if ing.purchase_date == ingredient_date.strftime(date_format):
                        if ingredient_amount > ing.amount:
                            raise InvalidArgException(
                                f"The amount you wanted to remove from the household {household.household_name}"
                                f" is greater than the amount that is in ingredient {ingredient_name} on this date. The maximum amount is {ing.amount}")
                        if ing.amount >= ingredient_amount:
                            ing.amount -= ingredient_amount
                        if ing.amount <= 0:
                            household.ingredients[ingredient_name].remove(ing)
                        self.firebase_instance.update_firebase_data(f'households/{household_id}'
                                                                    , to_household_entity(household).__dict__)
                        return
            raise InvalidArgException(
                f"No such ingredient '{ingredient_name}' in household '{household.household_name}' with date {ingredient_date.strftime(date_format)}")
        except KeyError as e:
            raise InvalidArgException(f"No such ingredient {ingredient_name} in household {household.household_name}")

    async def remove_household_ingredient(self, user_mail: str, household_id, ingredient_name: str,
                                          ingredient_amount: float):
        if ingredient_amount < 0:
            raise InvalidArgException("Invalid ingredient amount, it cannot be a negative number")

        household = await self.get_household_user_by_id(user_mail, household_id)
        ingredient_name = ingredient_name.capitalize()  # Convert to title case

        if ingredient_name not in household.ingredients:
            raise InvalidArgException(f"'{ingredient_name}' not found in household ingredients")

        ingredient_lst = household.ingredients[ingredient_name]
        ingredient_lst.sort(key=lambda x: x.purchase_date)
        sum_amounts = sum([ing.amount for ing in ingredient_lst])

        if sum_amounts < ingredient_amount:
            raise InvalidArgException(
                f"The max amount to remove of ingredient '{ingredient_name}' is {sum_amounts}")

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

        household.ingredients[ingredient_name] = updated_ingredients
        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)

    async def get_all_ingredients_in_household(self, user_email, household_id) -> dict:
        household = await self.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            for ingredient_name, data in household.ingredients.items():
                household.ingredients[ingredient_name].sort(key=lambda x: x.purchase_date)
            return household.ingredients

    async def correct_recipe_ingredient_name(self, recipe_ingredient: IngredientBoundary):
        recipe_ingredient.name = recipe_ingredient.name[0].upper() + recipe_ingredient.name[1:].lower()
        ingredient_data = self.ingredientsCRUD.search_ingredient(recipe_ingredient.name)
        if ingredient_data is None:
            raise ValueError(f"Ingredient {recipe_ingredient.name} Not Found")
        recipe_ingredient.ingredient_id = ingredient_data['id']
        recipe_ingredient.name = ingredient_data['name']

    async def check_ingredient_availability(self, household: HouseholdBoundary,
                                            recipe_ingredient: IngredientBoundary, recipe_id: str,
                                            dishes_number: float):
        try:
            sum_amount = sum(ingredient.amount for ingredient in household.ingredients[recipe_ingredient.name])
            if sum_amount < recipe_ingredient.amount * dishes_number:
                message = (f"Household '{household.household_name}' id : '{household.household_id}'"
                           f" does not have enough '{recipe_ingredient.name}' ingredient for"
                           f" recipe '{recipe_id}'. Needed: {recipe_ingredient.amount * dishes_number}, Available: {sum_amount}")
                logger.error(message)
                raise InvalidArgException(message)
        except KeyError:
            logger.error(f"Household '{household.household_name}' id : '{household.household_id}'"
                         f" does not have the '{recipe_ingredient.name}' ingredient")
            raise InvalidArgException(f"Household '{household.household_name}' id : '{household.household_id}'"
                                      f" does not have the '{recipe_ingredient.name}' ingredient")

    def add_meal_to_household(self, household: HouseholdBoundary, new_meal: MealBoundary):
        try:
            date_meals = household.meals[new_meal.used_date]
            try:
                type_meals = date_meals[new_meal.type]
                try:
                    meal = type_meals[new_meal.recipe_id]
                    for new_user in new_meal.users:
                        exist = False
                        for user in meal.users:
                            if user == new_user:
                                exist = True
                        if exist is False:
                            meal.users.append(new_user)
                    meal.number_of_dishes += new_meal.number_of_dishes
                except KeyError:
                    type_meals[new_meal.recipe_id] = new_meal
            except KeyError:
                date_meals[new_meal.type] = {new_meal.recipe_id:
                                                 new_meal}
        except KeyError:
            household.meals[new_meal.used_date] = {new_meal.type:
                                                       {new_meal.recipe_id:
                                                            new_meal}}

    def add_meal_to_user(self, user: UserBoundary, new_meal: MealBoundaryWithIngredients):
        try:
            meals = user.meals[new_meal.used_date]
            meals.append(new_meal)
        except KeyError:
            user.meals[new_meal.used_date] = [new_meal]

    async def use_recipe(self, user_email: str, household_id: str, recipe_id: str,
                         recipe_ingredients: [IngredientBoundary], mealType: meal_types, dishes_number: float):
        household = await self.get_household_user_by_id(user_email, household_id)
        if isinstance(household, HouseholdBoundary):
            for recipe_ingredient in recipe_ingredients:
                await self.correct_recipe_ingredient_name(recipe_ingredient)
                await self.check_ingredient_availability(household, recipe_ingredient, recipe_id, dishes_number)
            '''Removing the ingredients in a household'''
            for recipe_ingredient in recipe_ingredients:
                await self.remove_household_ingredient(user_email, household_id, recipe_ingredient.name,
                                                       recipe_ingredient.amount * dishes_number)
            household = await self.get_household_user_by_id(user_email, household_id)
            new_meal = MealBoundary(datetime.now(), mealType, [user_email], recipe_id, dishes_number)
            self.add_meal_to_household(household, new_meal)
            new_meal = MealBoundaryWithIngredients(
                datetime.strptime(new_meal.used_date, date_format).date(),
                new_meal.type,
                new_meal.users,
                new_meal.recipe_id,
                new_meal.number_of_dishes,
                [Ing(ingredient.name, ingredient.amount * dishes_number) for ingredient in recipe_ingredients])

            user = await self.get_user(user_email)
            if isinstance(user, UserBoundary):
                self.add_meal_to_user(user, new_meal)
                self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',
                                                            to_user_entity(user).__dict__)
                self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                            to_household_entity(household).__dict__)

    async def delete_user(self, user_email):
        user = await self.get_user(user_email)
        if isinstance(user, UserBoundary):
            for household_id in user.households:
                household = await self.get_household_user_by_id(user_email,household_id)
                if isinstance(household, HouseholdBoundary):
                    household.participants.remove(user.user_email)
                    self.firebase_instance.update_firebase_data(f'households/{household_id}'
                                                                ,to_household_entity(household).__dict__)
            self.firebase_instance.delete_firebase_data(f'users/{encoded_email(user_email)}')


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
