import unittest
from datetime import datetime
from typing import List
from unittest import TestCase

from BL.recipes_service import toBoundaryRecipe
from BL.users_household_service import to_household_boundary
from Data.recipe_entity import RecipeEntityByIngredientSpoonacular
from routers_boundaries.HouseholdBoundary import HouseholdBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.InputsForApiCalls import UserInputForAddUser, ListIngredientsInput, IngredientInput
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
        base_url + f'/users_household/get_all_recipes_that_household_can_make?user_email={user_email}?household_id={household_id}')


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


class UserTests(TestCase):
    def test_check_if_user_exists(self, user_email: str):
        response = get_user(user_email)
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        user_boundary = UserBoundary(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            user_email=user_data["user_email"],
            image=user_data["image"],
            households_ids=user_data["households"],
            meals=user_data["meals"],
            country=user_data["country"],
            state=user_data["state"]
        )
        self.assertEqual(user_boundary.user_email, user_email)

    def test_delete_user(self, user_email: str):
        response = delete_user(user_email)
        self.assertEqual(response.status_code, 200)
        response = get_user(user_email)
        self.assertEqual(response.status_code, 404)

    def test_add_user_to_system(self):
        user = build_user_input()
        self.assertEqual(add_user(user).status_code, 200)
        self.test_check_if_user_exists(user.email)
        self.test_delete_user(user.email)
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


def build_household_boundary(data):
    ingredients_dict = {}
    for ingredient_id, ingredients in data["ingredients"].items():
        ing_lst = []
        for ing in ingredients:
            ing = IngredientBoundary(
                ing["ingredient_id"],
                ing["name"],
                ing["amount"],
                ing["unit"],
                datetime.strptime(ing["purchase_date"], "%Y-%m-%d")
            )
            ing_lst.append(ing)
        ingredients_dict[ingredient_id] = ing_lst
    return HouseholdBoundary(
        data["household_id"],
        data["household_name"],
        data["household_image"],
        data["participants"],
        ingredients_dict,
        data["meals"]
    )


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
        data = get_household_by_household_id_and_userEmail(self.user_email, self.household_id).json()
        household = to_household_boundary(data)
        ingredients_in_household = []
        for ingredient_id, ingredients in household.ingredients.items():
            unique_names = list(set([ing.name for ing in ingredients]))
            ingredients_in_household+= unique_names
        if ingredients_in_household.__len__() == 0:
            self.fail("There are no ingredients in the household")
        data = get_recipes(self.user_email, self.household_id).json()
        if isinstance(data,list):
            recipes = []
            for recipe in data:
                recipes.append(toBoundaryRecipe( RecipeEntityByIngredientSpoonacular(recipe)))
            for recipe in recipes:
                self.assertIn(recipe.recipe_id,household.ingredients.keys())


if __name__ == '__main__':
    unittest.main()
