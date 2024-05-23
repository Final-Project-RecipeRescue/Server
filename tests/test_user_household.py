import unittest
from unittest import TestCase
from routers_boundaries.InputsForApiCalls import UserInputForAddUser, ListIngredientsInput, IngredientInput
from routers_boundaries.UserBoundary import UserBoundary
import requests
import logging
import random

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


def build_ingredients_input():
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


def get_status_code_from_body(response: requests.Response):
    return response.json().get("status_code")


def check_if_household_exist(household_id: str):
    return requests.get(base_url + f'/users_household/check_if_household_exist_in_system?household_id={household_id}')


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
        self.assertEqual(get_status_code_from_body(response), 404)

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
        self.assertEqual(get_status_code_from_body(response), 400)
        user.email = "server_test"
        response = add_user(user)
        self.assertEqual(get_status_code_from_body(response), 400)
        user.email = None
        response = add_user(user)
        self.assertEqual(response.status_code, 422)
        user.email = "@a.c"
        response = add_user(user)
        self.assertEqual(get_status_code_from_body(response), 400)
        logger.info("Test : test_add_wrong_users pass successfully")


class HouseholdTests(TestCase):
    def test_check_if_household_exists(self, household_id: str, user_email: str):
        response = get_household_by_hosehold_id_and_userEmail(user_email, household_id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(get_status_code_from_body(response), 404)
        self.assertEqual(response.json().get("household_id"), household_id)
        participants = response.json().get("participants")
        self.assertIn(user_email, participants)

    def test_delete_household(self, household_id: str):
        response = delete_household_by_id(household_id)
        self.assertEqual(response.status_code, 200)
        response = check_if_household_exist(household_id)
        self.assertEqual(get_status_code_from_body(response), 404)
        self.assertEqual(response.json().get("detail"), f"Household {household_id} does not exist in system")

    def test_crate_household(self, ingredients : ListIngredientsInput = build_ingredients_input()):
        user = build_user_input()
        add_user(user)
        household_name = "server_test"
        response = create_new_household(user.email, household_name, ingredients)

        self.assertEqual(get_status_code_from_body(response), None)
        self.assertEqual(response.json().get("message"), "Household added successfully")

        household_id = response.json()["household_id"]
        self.test_check_if_household_exists(household_id, user.email)
        response = get_household_by_hosehold_id_and_userEmail(user.email, household_id)
        self.assertEqual(response.json()["household_name"], household_name)

        delete_user(user.email)
        self.test_delete_household(household_id)
        logger.info("Test : test_crate_household pass successfully")

    def test_crate_household_with_Ingredients(self):
        ingredients = build_ingredients_input()
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
        self.test_crate_household(ingredients)
        logger.info("Test : test_crate_household_with_Ingredients pass successfully")


if __name__ == '__main__':
    unittest.main()
