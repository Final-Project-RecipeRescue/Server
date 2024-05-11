import unittest
from unittest import TestCase
from routers_boundaries.InputsForApiCalls import UserInputForAddUser, ListIngredientsInput
from routers_boundaries.UserBoundary import UserBoundary
import requests

base_url = "http://127.0.0.1:8000"


def add_user(user_input: UserInputForAddUser):
    return requests.post(base_url + "/users_household/add_user", json=user_input.model_dump())


def get_user(user_email: str):
    return requests.get(base_url + f"/users_household/get_user?user_email={user_email}")


def delete_user(user_email: str):
    return requests.delete(base_url + f"/users_household/delete_user?user_email={user_email}")


def build_user_input():
    return UserInputForAddUser(
        first_name="test1",
        last_name="test1",
        email="test1@test1.test1",
        country="test1",
        state="test1"
    )


def build_ingredients_input():
    return ListIngredientsInput(
        ingredients=[]
    )


def create_new_household(user_email: str, household_name: str, ingredients: ListIngredientsInput):
    return requests.post(base_url +
                         f"/users_household/createNewHousehold?user_mail={user_email}&household_name={household_name}"
                         , json=ingredients.model_dump())


def get_household_by_id(user_email: str, household_id: str):
    return requests.get(
        base_url + f"/users_household/get_household_user_by_id?user_email={user_email}&household_id={household_id}")


def delete_household_by_id(household_id: str):
    return requests.delete(base_url + f'/users_household/delete_household?household_id={household_id}')


class Test(TestCase):
    def test_add_user_to_system(self):
        def test_check_if_user_exists(user_email: str):
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

        def test_delete_user(user_email: str):
            response = requests.delete(base_url + f"/users_household/delete_user?user_email={user_email}")
            self.assertEqual(response.status_code, 200)
            response = requests.get(base_url + f"/users_household/get_user?user_email={user_email}")
            self.assertEqual(response.status_code, 404)

        user = build_user_input()
        self.assertEqual(add_user(user).status_code, 200)
        test_check_if_user_exists(user.email)
        test_delete_user(user.email)

    def test_add_wrong_users(self):
        user = build_user_input()
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        user.email = ""
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        user.email = "test1"
        response = add_user(user)
        self.assertEqual(response.status_code, 400)
        user.email = None
        response = add_user(user)
        self.assertEqual(response.status_code, 422)
        user.email = "@a.c"
        response = add_user(user)
        self.assertEqual(response.status_code, 400)

    def test_crate_household(self):
        user = build_user_input()
        add_user(user)
        household_name = "test1"
        ingredients = build_ingredients_input()
        response = create_new_household(user.email, household_name, ingredients)
        household_id = response.json()["household_id"]
        self.assertEqual(response.status_code, 200)
        response = get_household_by_id(user.email, household_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["household_name"], household_name)
        delete_household_by_id(household_id)
        delete_user(user.email)


if __name__ == '__main__':
    unittest.main()
