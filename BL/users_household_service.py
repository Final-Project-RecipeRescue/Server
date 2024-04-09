from typing import List
from Data.household_entity import HouseholdEntity
import uuid
from DAL.firebase_db_connection import FirebaseDbConnection
from Data.user_entity import UserEntity
import Data.user_entity as user_entity_py


def encoded_email(email: str) -> str:
    return email.replace('.',',')
def decoded_email(email: str) -> str:
    return email.replace(',','.')
class UsersHouseholdService:
    def __init__(self):
        self.firebase_instance = FirebaseDbConnection.get_instance()

    #TODO:need to add option to enter image
    async def create_household(self, user_mail: str, household_name: str) -> int:
        try:
            if user_entity_py.is_valid_email(user_mail) == False:
                #raise exceptions.UserMailNotVail
                print("Invalid")
                return -1
            if self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}') == None:
                ##raise exceptions.UserDoesNotExistException()
                print("user not exist")
                return -1
            if self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}/households/{household_name}') != None:
                ###raise exceptions.HouseholdAllReadyExistException
                return -1
            household_id = str(uuid.uuid4())
            while(self.firebase_instance.get_firebase_data(f'households/{household_id}') != None):
                household_id = str(uuid.uuid4())

            household = HouseholdEntity(household_id,
                                               household_name,
                                               None,
                                               [self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}/user_email')],
                                               [],
                                               [])

            self.firebase_instance.write_firebase_data(f'households/{household_id}',household.__dict__)

            user_data = self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}')
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            email = user_data['user_email']
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
            if households is not None:
                households.append(household_id)
            else:
                households = [household_id]
            user = UserEntity(first_name,last_name,email,image,households,meals)
            self.firebase_instance.update_firebase_data(f'users/{encoded_email(user_mail)}',user.__dict__)
            return 1
        except Exception as e:
            print(e)
            return -1

    # TODO:need to add option to enter image
    async def create_user(self, user_first_name:str, user_last_name:str, user_mail:str) -> int:
        try:
            if self.firebase_instance.get_firebase_data(f'users/{encoded_email(user_mail)}') != None:
                ###raise exceptions.UserAllReadyExistException
                print("user already exists")
                return -1
            if user_entity_py.is_valid_email(user_mail) == False:
                print("invalid")
                return -1
            user = UserEntity(user_first_name,
                              user_last_name,
                              user_mail,
                              None,
                              [],
                              [])
            self.firebase_instance.write_firebase_data(f'users/{encoded_email(user_mail)}',user.__dict__)
            return 1
        except Exception as e:
            print(e)
            return -1