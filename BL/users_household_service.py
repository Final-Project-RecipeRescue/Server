import datetime
from datetime import datetime
import json
from typing import List

from Data.HouseholdEntity import HouseholdEntity
from routers_boundaries.HouseholdBoundary import HouseholdBoundary
import uuid
from DAL.firebase_db_connection import FirebaseDbConnection
from routers_boundaries.Ingredient_boundary import ingredient_boundary
from routers_boundaries.UserBoundary import UserBoundary
import routers_boundaries.UserBoundary as user_entity_py
from Data.IngredientEntity import IngredientEntity


def encoded_email(email: str) -> str:
    return email.replace('.', ',')


def decoded_email(email: str) -> str:
    return email.replace(',', '.')


with open('config/ingredientId_map.json', 'r') as file:
    ingredientId_map = json.load(file)
date_format = "%Y-%m-%d %H:%M:%S.%f"


def to_ingredient_boundary(ingredient: object) -> ingredient_boundary:
    try:
        return ingredient_boundary(
            int(ingredient['id']),
            ingredient['name'],
            float(ingredient['amount']),
            ingredient['unit'],
            datetime.strptime(ingredient['purchase_date'], date_format))
    except KeyError:
        return None


def to_user_boundary(user_data: object) -> UserBoundary:
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    email = user_data['user_email']
    country = user_data['country']
    state = user_data['state']
    image = None
    households = []
    meals = []
    try:
        image = user_data['image']
    except KeyError:
        pass
    try:
        households = user_data['households']
    except KeyError:
        pass
    try:
        meals = user_data['meals']
    except KeyError:
        pass
    return UserBoundary(first_name, last_name, email, image, households, meals, country, state)


def to_household_boundary(household_data: object) -> HouseholdBoundary:
    household_id = household_data['household_id']
    household_name = household_data['household_name']
    household_image = None
    try:
        household_image = household_data['household_image']
    except KeyError:
        pass
    participants = household_data['participants']
    ingredients = []
    try:
        for ingredient_id, ingredient_details in household_data['ingredients'].items():
            ingredients.append(to_ingredient_boundary(ingredient_details))
    except KeyError:
        pass
    meals = []
    try:
        meals = household_data['meals']
    except KeyError:
        pass
    return HouseholdBoundary(household_id, household_name, household_image, participants, ingredients, meals)


def to_ingredient_entity(ingredient: ingredient_boundary) -> IngredientEntity:
    return IngredientEntity(
        ingredient.ingredient_id,
        ingredient.name,
        ingredient.amount,
        ingredient.unit,
        ingredient.purchase_date)


def to_household_entity(household: HouseholdBoundary) -> HouseholdEntity:
    ingredients = {}
    for ingredient in household.ingredients:
        ingredients[ingredient.ingredient_id] = to_ingredient_entity(ingredient).__dict__
    return HouseholdEntity(
        household.household_id,
        household.household_name,
        household.household_image,
        household.participants,
        ingredients,
        {})


class UsersHouseholdService:
    def __init__(self):
        self.firebase_instance = FirebaseDbConnection.get_instance()

    def check_email(self, email: str):
        if not user_entity_py.is_valid_email(email):
            raise InvalidArgException("Invalid email format")

    async def check_user_if_user_exist(self, email: str):
        if self.firebase_instance.get_firebase_data(f'users/{encoded_email(email)}') == None:
            raise UserException("User not exists")

    # TODO:need to add option to enter image
    async def create_household(self, user_mail: str, household_name: str):
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
                                      [],
                                      [])

        self.firebase_instance.write_firebase_data(f'households/{household_id}', household.__dict__)

        if user.households is not None:
            user.households.append(household_id)
        else:
            user.households = [household_id]
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_mail)}', user.__dict__)

    # TODO:need to add option to enter image
    async def create_user(self, user_first_name: str, user_last_name: str, user_mail: str, country: str, state: str):
        self.check_email(user_mail)
        if self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}') != None:
            raise UserException("User already exists")
        if user_first_name == "" or user_last_name == "" or country == "" or state == "":
            raise InvalidArgException("Fill all fields before")
        user = UserBoundary(user_first_name,
                            user_last_name,
                            user_mail,
                            None,
                            [],
                            [],
                            country,
                            state)
        self.firebase_instance.write_firebase_data(f'users/{encoded_email(user_mail)}', user.__dict__)

    async def get_user(self, email: str) -> UserBoundary:
        self.check_email(email)
        e_email = encoded_email(email)
        user = self.firebase_instance.get_firebase_data(f'users/{e_email}')
        if not user:
            raise UserException("User does not exist")
        user_boundray = to_user_boundary(user)
        return user_boundray

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
            self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}', user_boundary.__dict__)

    async def add_ingredient_to_household_by_ingredient_id(self, user_email: str, household_id: str, ingredient_id: int,
                                                           ingredient_amount: float):
        household = await self.get_household_user_by_id(user_email, household_id)
        try:
            ingredient_name = ingredientId_map[f'{ingredient_id}']
        except KeyError as e:
            raise InvalidArgException(f'Ingredient id {ingredient_id} does not exist')


        ingredient = ingredient_boundary(ingredient_id, ingredient_name, ingredient_amount, "", datetime.now())
        household.ingredients.append(ingredient)
        self.firebase_instance.update_firebase_data(f'households/{household_id}',
                                                    to_household_entity(household).__dict__)


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
