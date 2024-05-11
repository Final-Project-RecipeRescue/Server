import unittest
from unittest import TestCase
from routers_boundaries.InputsForApiCalls import UserInputForAddUser
from routers_boundaries.UserBoundary import UserBoundary
import requests

base_url = "http://127.0.0.1:8000"

class Test(TestCase):
    def test_add_user_to_system(self):
        user = UserInputForAddUser(
            first_name="Test",
            last_name="User",
            email="test@test.test",
            country="Israel",
            state="Haifa"
        )
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 200)
        response = requests.get(base_url + f"/users_household/get_user?user_email={user.email}")
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
        self.assertEqual(user_boundary.user_email, user.email)
        response = requests.delete(base_url+f"/users_household/delete_user?user_email={user.email}")
        self.assertEqual(response.status_code,200)
        response = requests.get(base_url + f"/users_household/get_user?user_email={user.email}")
        self.assertEqual(response.status_code, 404)

    def test_add_wrong_users(self):
        user = UserInputForAddUser(
            first_name="Test",
            last_name="User",
            email="test@.test",
            country="Israel",
            state="Haifa"
        )
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 400)
        user.email = ""
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 400)
        user.email = "test"
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 400)
        user.email = None
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 422)
        user.email = "@a.c"
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 400)




if __name__ == '__main__':
    unittest.main()
