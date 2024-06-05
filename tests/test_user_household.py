import unittest
from datetime import datetime
from typing import List, Dict, Any
from unittest import TestCase

from BL.recipes_service import toBoundaryRecipe
from BL.users_household_service import to_household_boundary
from Data.recipe_entity import RecipeEntityByIngredientSpoonacular
from routers_boundaries.HouseholdBoundary import HouseholdBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.InputsForApiCalls import UserInputForAddUser, ListIngredientsInput, IngredientInput, \
    UserInputForChanges
from routers_boundaries.MealBoundary import meal_types, MealBoundary
from routers_boundaries.UserBoundary import UserBoundary
import requests
import logging
import random

from routers_boundaries.recipe_boundary import RecipeBoundary

logger = logging.getLogger("my_test_logger")
logger.setLevel(logging.DEBUG)
stream_handler = logging.FileHandler("server_tests_log_file.log", mode='w')
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

base_url = "http://127.0.0.1:8000"


def add_user(user_input: UserInputForAddUser):
    return requests.post(base_url + "/users_household/add_user", json=user_input.model_dump())


def get_user(user_email: str):
    return requests.get(base_url + f"/users_household/get_user?user_email={user_email}")


def delete_user(user_email: str):
    return requests.delete(base_url + f"/users_household/delete_user?user_email={user_email}")


def build_user_input():
    return UserInputForAddUser(
        first_name="server_test",
        last_name="server_test",
        email="server_test@server_test.server_test",
        country="server_test",
        state="server_test"
    )


def build_ingredients_empty_input():
    return ListIngredientsInput(
        ingredients=[]
    )


def create_new_household(user_email: str, household_name: str, ingredients: ListIngredientsInput):
    return requests.post(base_url +
                         f"/users_household/createNewHousehold?user_mail={user_email}&household_name={household_name}"
                         , json=ingredients.model_dump())


def get_household_by_household_id_and_userEmail(user_email: str, household_id: str):
    return requests.get(
        base_url + f"/users_household/get_household_user_by_id?user_email={user_email}&household_id={household_id}")


def delete_household_by_id(household_id: str):
    return requests.delete(base_url + f'/users_household/delete_household?household_id={household_id}')


def check_if_household_exist(household_id: str):
    return requests.get(base_url + f'/users_household/check_if_household_exist_in_system?household_id={household_id}')


def get_recipes(user_email: str, household_id: str):
    return requests.get(
        base_url + f'/users_household/get_all_recipes_that_household_can_make?user_email={user_email}&household_id={household_id}')

def get_ingredients():
    ingredients = build_ingredients_empty_input()
    ingredients_names = [
        "Olive oil",
        "Garlic",
        "Onion",
        "Tomatoes",
        "Chicken breast",
        "Ground beef",
        "Carrots",
        "Potatoes",
        "Bell peppers",
        "Spinach",
        "Broccoli",
        "Mushrooms",
        "Rice",
        "Pasta",
        "Eggs",
        "Parmesan cheese",
        "Black beans",
        "Flour",
        "Sugar",
        "Butter"
    ]
    for ingredient in ingredients_names:
        random_number = random.randint(1, 1000)
        ingredientInput = IngredientInput(
            ingredient_id=None,
            name=ingredient,
            amount=random_number,
            unit=None
        )
        ingredients.ingredients.append(ingredientInput)
    return ingredients

def update_user_information(user_input : UserInputForChanges):
    return requests.put(base_url + "/users_household/update_personal_user_info", json=user_input.model_dump())

class UserTests(TestCase):
    user_email = None
    def tearDown(self):
        if self.user_email:
            delete_user(self.user_email)
            self.user_email = None

    def test_add_user_to_system(self):
        user = build_user_input()
        response = add_user(user)
        self.assertEqual(response.status_code, 200)
        self.user_email = user.email
        logger.info("Test : test_add_user_to_system pass successfully")
    def test_add_wrong_users(self):
        user = build_user_input()
        user.email = ""
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        user.email = "server_test"
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        user.email = None
        response = add_user(user)
        self.assertEqual(response.status_code, 422)
        user.email = "@a.c"
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        logger.info("Test : test_add_wrong_users pass successfully")
    def test_get_user(self):
        self.test_add_user_to_system()
        response = get_user(self.user_email)
        self.assertEqual(response.status_code,200)
        logger.info("Test : test_login_user pass successfully")
    def test_get_user_not_found(self):
        self.test_add_user_to_system()
        email = self.user_email
        self.tearDown()
        response = get_user(email)
        self.assertEqual(response.status_code,404)
        logger.info("Test : test_login_user with user dont exist pass successfully")
    def test_add_user_already_exists(self):
        self.test_add_user_to_system()
        user = build_user_input()
        user.email = self.user_email
        user.country = "test"
        response = add_user(user)
        self.assertEqual(response.status_code,409)
        logger.info("Test : test_add_user_already_exists pass successfully")
    def test_change_user_info(self):
        self.test_add_user_to_system()
        user = build_user_input()
        new_name = f"{user.first_name}test"
        new_last_name = f"{user.last_name}test"
        new_country = None
        new_state = f"{user.state}test"
        user = UserInputForChanges(
            email=self.user_email,
            first_name=new_name,
            last_name=new_last_name,
            country=new_country,
            state=new_state
        )
        response = update_user_information(user)
        self.assertEqual(response.status_code,200)
        response = get_user(self.user_email)
        self.assertEqual(response.json()['first_name'],new_name) \
            if new_name is not None else self.assertEqual(response.json()['first_name'],build_user_input().first_name)
        self.assertEqual(response.json()['last_name'], new_last_name) \
            if new_last_name is not None else self.assertEqual(response.json()['last_name'],build_user_input().last_name)
        self.assertEqual(response.json()['country'], new_country) \
            if new_country is not None else self.assertEqual(response.json()['country'],build_user_input().country)
        self.assertEqual(response.json()['state'], new_state) \
            if new_state is not None else self.assertEqual(response.json()['state'],build_user_input().state)
        self.assertEqual(response.json()['user_email'],self.user_email)
        logger.info("Test : test_change_user_info pass")

class HouseholdTests(TestCase):
    household_id = None
    user_email = None

    def tearDown(self):
        # This function will be executed after every test method
        if self.user_email is not None:
            delete_user(self.user_email)
        if self.household_id is not None:
            delete_household_by_id(self.household_id)
        self.household_id = None
        self.user_email = None

    def test_crate_household(self, ingredients: ListIngredientsInput = build_ingredients_empty_input()):
        user = build_user_input()
        add_user(user)
        self.user_email = user.email
        household_name = "server_test"
        response = create_new_household(user.email, household_name, ingredients)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Household added successfully")
        self.household_id = response.json()["household_id"]

        response = get_household_by_household_id_and_userEmail(user.email, self.household_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("household_id"), self.household_id)
        self.assertEqual(response.json()["household_name"], household_name)
        participants = response.json().get("participants")
        self.assertIn(self.user_email, participants)
        logger.info("Test : test_crate_household pass successfully")

    def test_crate_household_with_Ingredients(self):
        self.test_crate_household(get_ingredients())
        logger.info("Test : test_crate_household_with_Ingredients pass successfully")

    def test_get_recipes(self):
        user = build_user_input()
        add_user(user)
        self.user_email = user.email
        household_name = "server_test"
        ingredients_to_add = get_ingredients()
        response = create_new_household(user.email, household_name, ingredients_to_add)
        self.household_id = response.json()["household_id"]
        response = get_recipes(self.user_email, self.household_id)
        self.assertEqual(response.status_code,200)
        logger.info(f"Test : test_get_recipes pass successfully the recipes is : {response.json()}")

if __name__ == '__main__':
    unittest.main()
