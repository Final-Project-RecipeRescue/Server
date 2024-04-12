from typing import List
from Data.household_entity import HouseholdEntity
import uuid
from DAL.firebase_db_connection import FirebaseDbConnection
from Data.user_entity import UserEntity
import Data.user_entity as user_entity_py


def encoded_email(email: str) -> str:
    return email.replace('.', ',')


def decoded_email(email: str) -> str:
    return email.replace(',', '.')


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
        if not user_data:
            raise UserException("User not found")

        household_id = str(uuid.uuid4())
        while (self.firebase_instance.get_firebase_data(f'households/{household_id}') != None):
            household_id = str(uuid.uuid4())

        household = HouseholdEntity(household_id,
                                    household_name,
                                    None,
                                    [self.firebase_instance.get_firebase_data(
                                        f'users/{encoded_email(user_mail)}/user_email')],
                                    [],
                                    [])

        self.firebase_instance.write_firebase_data(f'households/{household_id}', household.__dict__)

        user = self.to_user_entity(user_data)
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
        user = UserEntity(user_first_name,
                          user_last_name,
                          user_mail,
                          None,
                          [],
                          [],
                          country,
                          state)
        self.firebase_instance.write_firebase_data(f'users/{encoded_email(user_mail)}', user.__dict__)

    async def get_user(self, email: str) -> UserEntity:
        self.check_email(email)
        e_email = encoded_email(email)
        user = self.firebase_instance.get_firebase_data(f'users/{e_email}')
        if not user:
            raise UserException("User does not exist")
        user_entity = self.to_user_entity(user)
        return user_entity

    async def get_household_user_by_id(self, user_email: str, household_id: str) -> HouseholdEntity:
        user_entity = await self.get_user(user_email)
        for id in user_entity.households:
            if id == household_id:
                household = self.firebase_instance.get_firebase_data(f'households/{id}')
                if not household:
                    raise HouseholdException("Household does not exist")
                household_entity = self.to_household_entity(household)
                return household_entity
        raise HouseholdException("Household does not exist")

    async def get_household_user_by_name(self, user_email, household_name) -> List[HouseholdEntity]:
        user_entity = await self.get_user(user_email)

        households = []
        for id in user_entity.households:
            household = self.firebase_instance.get_firebase_data(f'households/{id}')
            if not household:
                raise HouseholdException(
                    "You have a problem in the DB with the user the household is found but with the collection of households it is not found")
            household_entity = self.to_household_entity(household)
            if household_entity.household_name == household_name:
                households.append(household_entity)
        if households.__len__() == 0:
            raise HouseholdException("Household does not exist")
        return households

    async def add_user_to_household(self, user_email:str, household_id:str):
        user_entity = await self.get_user(user_email)
        household = self.firebase_instance.get_firebase_data(f'households/{household_id}')
        if not household:
            raise HouseholdException('Household does not exist')
        household = self.to_household_entity(household)
        for user in household.participants:
            if user == user_entity.user_email:
                raise HouseholdException('User already exists in the household')
        household.participants.append(user_email)
        user_entity.households.append(household.household_id)
        self.firebase_instance.update_firebase_data(f'households/{household_id}',household.__dict__)
        self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_email)}',user_entity.__dict__)



    def to_user_entity(self, user_data: object) -> UserEntity:
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        email = user_data['user_email']
        country = user_data['country']
        state = user_data['state']
        image = None
        households = None
        meals = None
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
        return UserEntity(first_name, last_name, email, image, households, meals, country, state)

    def to_household_entity(self, household_data: object) -> HouseholdEntity:
        household_id = household_data['household_id']
        household_name = household_data['household_name']
        household_image = None
        try:
            household_image = household_data['household_image']
        except KeyError:
            pass
        participants = household_data['participants']
        ingredients = None
        try:
            ingredients = household_data['ingredients']
        except KeyError:
            pass
        meals = None
        try:
            meals = household_data['meals']
        except KeyError:
            pass
        return HouseholdEntity(household_id, household_name, household_image, participants, ingredients, meals)




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
