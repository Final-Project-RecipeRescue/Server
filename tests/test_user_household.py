import unittest
from unittest import TestCase
from unittest.mock import patch,Mock
from routers import user_household
from routers.user_household import get_meal_types
from routers.user_household import add_user
from routers_boundaries.InputsForApiCalls import UserInputForAddUser


class Test(TestCase):
    def test_get_meal_types(self):
        self.assertEqual(get_meal_types(), ['Breakfast', 'Lunch', 'Dinner', 'Snakes'])

    def test_get_meal_types_empty(self):
        self.assertNotEquals(get_meal_types(),None)


    @patch("create")
    def test_add_user(self,mock_get):
        mock_response = Mock()
        response_dict = {"message": "Successfully Added User"}
        mock_response.json.return_value = response_dict
        mock_get.return_value = mock_response
        user_input = UserInputForAddUser()
        user_input.first_name = 'John'
        user_input.last_name = 'Doe'
        user_input.email = 'john@example.com'
        user_input.country = 'USA'
        user_input.state = 'California'
        response = add_user(user_input)

if __name__ == '__main__':
    unittest.main()
