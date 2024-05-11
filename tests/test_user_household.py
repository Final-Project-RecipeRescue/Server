import unittest
from unittest import TestCase
from routers_boundaries.InputsForApiCalls import UserInputForAddUser
from routers_boundaries.UserBoundary import UserBoundary
import requests

base_url = "http://127.0.0.1:8000"

class Test(TestCase):
    def test_add_user(self):
        user = UserInputForAddUser(
            first_name="Test",
            last_name="User",
            email="test@test.test",
            country="Israel",
            state="Haifa"
        )
        response = requests.post(base_url + "/users_household/add_user", json=user.model_dump())
        self.assertEqual(response.status_code, 200)  # Adjusted for 200 status code
        # Now, let's get the user and verify it was added
        response = requests.get(base_url + f"/users_household/get_user?user_email={user.email}")
        self.assertEqual(response.status_code, 200)
        user_data = response.json()  # Extract user data from response
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

if __name__ == '__main__':
    unittest.main()
