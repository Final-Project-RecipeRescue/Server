import unittest
from datetime import datetime
from typing import Dict, Optional, List
from unittest import TestCase

from routers_boundaries.HouseholdBoundary import HouseholdBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.InputsForApiCalls import UserInputForAddUser, ListIngredientsInput, IngredientInput, \
    UserInputForChanges
import requests
import logging
import random

from routers_boundaries.MealBoundary import MealBoundary, meal_types
from routers_boundaries.UserBoundary import UserBoundary
from routers_boundaries.recipe_boundary import RecipeBoundary, RecipeBoundaryWithGasPollution

logger = logging.getLogger("my_test_logger")
logger.setLevel(logging.DEBUG)
stream_handler = logging.FileHandler("server_tests_log_file.log", mode='w')
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

base_url = "http://127.0.0.1:8000"


def add_user(user_input: UserInputForAddUser):
    return requests.post(base_url + "/usersAndHouseholdManagement/addUser", json=user_input.model_dump())


def get_user(user_email: str):
    return requests.get(base_url + f"/usersAndHouseholdManagement/getUser?user_email={user_email}")


def delete_user(user_email: str):
    return requests.delete(base_url + f"/usersAndHouseholdManagement/deleteUser?user_email={user_email}")


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
                         f"/usersAndHouseholdManagement/createNewHousehold?user_email={user_email}&household_name={household_name}"
                         , json=ingredients.model_dump())


def get_household_by_household_id_and_userEmail(user_email: str, household_id: str):
    return requests.get(
        base_url + f"/usersAndHouseholdManagement/getHouseholdUserById?user_email={user_email}&household_id={household_id}")


def delete_household_by_id(household_id: str):
    return requests.delete(base_url + f'/usersAndHouseholdManagement/deleteHousehold?household_id={household_id}')


def check_if_household_exist(household_id: str):
    return requests.get(base_url + f'/usersAndHouseholdManagement/checkIfHouseholdExistInSystem?household_id={household_id}')


def get_recipes(user_email: str, household_id: str):
    return requests.get(
        base_url + f'/usersAndHouseholdManagement/getAllRecipesThatHouseholdCanMake?user_email={user_email}&household_id={household_id}')


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
        "Butter",
        "Basil",
        "Cilantro",
        "Lemon",
        "Lime",
        "Cumin",
        "Paprika",
        "Coriander",
        "Ginger",
        "Soy sauce",
        "Honey",
        "Coconut milk",
        "Chili powder",
        "Oregano",
        "Thyme",
        "Rosemary",
        "Vanilla extract",
        "Almonds",
        "Walnuts",
        "Cashews",
        "scallions",
        "shallot"
    ]
    for ingredient in ingredients_names:
        random_number = random.randint(10000, 100000)
        ingredientInput = IngredientInput(
            ingredient_id=None,
            name=ingredient,
            amount=random_number,
            unit=None
        )
        ingredients.ingredients.append(ingredientInput)
    return ingredients


def update_user_information(user_input: UserInputForChanges):
    return requests.put(base_url + "/usersAndHouseholdManagement/updatePersonalUserInfo", json=user_input.model_dump())


def remove_user_from_household(user_email: str, household_id: str):
    return requests.delete(
        base_url + f"/usersAndHouseholdManagement/removeUserFromHousehold?user_email={user_email}&household_id={household_id}")


def add_ingredient_to_household(household_id: str, user_email: str, ingredient: IngredientInput):
    return requests.post(
        base_url + f"/usersAndHouseholdManagement/addIngredientToHouseholdByIngredientName?user_email={user_email}&household_id={household_id}",
        json=ingredient.model_dump())


def add_user_to_household(user_email: str, household_id: str):
    return requests.post(
        base_url + f"/usersAndHouseholdManagement/addUserToHousehold?user_email={user_email}&household_id={household_id}")


def check_if_household_can_make_recipe(household_id: str, recipe_id: str, dishes_num: Optional[int] = 1):
    return requests.get(base_url + f"/usersAndHouseholdManagement/"
                                   f"checkIfHouseholdCanMakeRecipe?"
                                   f"&household_id={household_id}"
                                   f"&recipe_id={recipe_id}"
                                   f"&dishes_num={dishes_num}")


def use_recipe(users_email: List[str], household_id: str,
               meal: str, dishes_num: float, recipe_id: str):
    return requests.post(
        base_url + f"/usersAndHouseholdManagement/useRecipeByRecipeId?household_id={household_id}&meal={meal}&dishes_num={dishes_num}&recipe_id={recipe_id}",json=users_email)


def parse_ingredient(ingredient_data: Dict) -> IngredientBoundary:
    return IngredientBoundary(
        ingredient_id=ingredient_data['ingredient_id'],
        name=ingredient_data['name'],
        amount=ingredient_data['amount'],
        unit=ingredient_data['unit'],
        purchase_date=ingredient_data['purchase_date']
    )


def parse_recipe(data: Dict) -> RecipeBoundaryWithGasPollution:
    ingredients = [parse_ingredient(ing) for ing in data['ingredients']]
    recipe = RecipeBoundary(
        recipe_id=data['recipe_id'],
        recipe_name=data['recipe_name'],
        ingredients=ingredients,
        image_url=data['image_url']
    )
    return RecipeBoundaryWithGasPollution(recipe, data['sumGasPollution'])


def parse_single_meal(data: Dict) -> MealBoundary:
    return MealBoundary(
        data.get('users', []),
        number_of_dishes=data['number_of_dishes']
    )


def parse_user_meals(meal_data: Dict) -> Dict[str, Dict[str, MealBoundary]]:
    parsed_meals = {}
    for day, meals in meal_data.items():
        parsed_meals[day] = {}
        for meal_type, recipes in meals.items():
            parsed_meals[day][meal_type] = {}
            for recipe_id, recipe in recipes.items():
                parsed_meals[day][meal_type][recipe_id] = parse_single_meal(recipe)
    return parsed_meals


def parse_household_meals(meal_data: Dict) -> Dict[str, Dict[str, MealBoundary]]:
    parsed_meals = {}
    for day, meals_types in meal_data.items():
        parsed_meals[day] = {}
        for meal_type, recipes_ids in meals_types.items():
            parsed_meals[day][meal_type] = {}
            for recipe_id, meals in recipes_ids.items():
                parsed_meals[day][meal_type][recipe_id] = []
                for meal in meals:
                    parsed_meals[day][meal_type][recipe_id].append(parse_single_meal(meal))
    return parsed_meals


def parse_user_boundary(data: Dict) -> UserBoundary:
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    user_email = data.get('user_email')
    image = data.get('image') if data.get('image') is not None else ""
    households_ids = data.get('households_ids', [])
    meals = parse_user_meals(data.get('meals', {})) if data.get('meals', {}) is not None else {}
    country = data.get('country')
    state = data.get('state') if data.get('state') is not None else None

    return UserBoundary(first_name, last_name, user_email, image, households_ids, meals, country, state)


def parse_household(data: Dict) -> HouseholdBoundary:
    household_id = data.get('household_id')
    household_name = data.get('household_name')
    household_image = data.get('household_image') if data.get('household_image') is not None else None
    participants = data.get('participants', [])
    meals = parse_household_meals(data.get('meals', {})) if data.get('meals', {}) is not None else {}
    ingredients_data = data.get('ingredients', {})
    ingredients = {}
    for ingredient_id, ingredient_list in ingredients_data.items():
        ingredients[ingredient_id] = []
        for ingredient_data in ingredient_list:
            ingredients[ingredient_id].append(parse_ingredient(ingredient_data))
    return HouseholdBoundary(household_id, household_name, household_image, participants, ingredients, meals)


class UserTests(TestCase):
    user_email = None

    def tearDown(self):
        if self.user_email:
            delete_user(self.user_email)
            self.user_email = None

    def test_add_user_to_system(self):
        user = build_user_input()
        response = add_user(user)
        self.assertEqual(200, response.status_code)
        self.user_email = user.email
        logger.info("Test : test_add_user_to_system pass successfully")

    def test_add_wrong_users(self):
        user = build_user_input()
        user.email = ""
        response = add_user(user)
        self.assertEqual(400, response.status_code)
        user.email = "server_test"
        response = add_user(user)
        self.assertEqual(400, response.status_code)
        user.email = None
        response = add_user(user)
        self.assertEqual(422, response.status_code)
        user.email = "@a.c"
        response = add_user(user)
        self.assertEqual(400, response.status_code)
        logger.info("Test : test_add_wrong_users pass successfully")

    def test_get_user(self):
        self.test_add_user_to_system()
        response = get_user(self.user_email)
        self.assertEqual(200, response.status_code)
        logger.info("Test : test_login_user pass successfully")

    def test_get_user_not_found(self):
        self.test_add_user_to_system()
        email = self.user_email
        self.tearDown()
        response = get_user(email)
        self.assertEqual(404, response.status_code)
        logger.info("Test : test_login_user with user dont exist pass successfully")

    def test_add_user_already_exists(self):
        self.test_add_user_to_system()
        user = build_user_input()
        user.email = self.user_email
        user.country = "test"
        response = add_user(user)
        self.assertEqual(409, response.status_code)
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
        self.assertEqual(200, response.status_code)
        response = get_user(self.user_email)
        self.assertEqual(response.json()['first_name'], new_name) \
            if new_name is not None else self.assertEqual(response.json()['first_name'], build_user_input().first_name)
        self.assertEqual(response.json()['last_name'], new_last_name) \
            if new_last_name is not None else self.assertEqual(response.json()['last_name'],
                                                               build_user_input().last_name)
        self.assertEqual(response.json()['country'], new_country) \
            if new_country is not None else self.assertEqual(response.json()['country'], build_user_input().country)
        self.assertEqual(response.json()['state'], new_state) \
            if new_state is not None else self.assertEqual(response.json()['state'], build_user_input().state)
        self.assertEqual(response.json()['user_email'], self.user_email)
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
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json().get("message"), "Household added successfully")
        self.household_id = response.json()["household_id"]

        response = get_household_by_household_id_and_userEmail(user.email, self.household_id)
        self.assertEqual(200, response.status_code)
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
        self.assertEqual(200, response.status_code)
        logger.info(f"Test : test_get_recipes pass successfully the recipes is : {response.json()}")

    def test_add_ingredient(self):
        self.test_crate_household()
        ingredients_to_add = IngredientInput(
            ingredient_id=None,
            name="Banana",
            amount=100,
            unit='gram'
        )
        response = add_ingredient_to_household(self.household_id, self.user_email, ingredients_to_add)
        self.assertEqual(200, response.status_code)
        response = get_household_by_household_id_and_userEmail(user_email=self.user_email,
                                                               household_id=self.household_id)
        self.assertEqual(response.json()['ingredients']['9040'][0]['name'].lower(), ingredients_to_add.name.lower())
        logger.info(f"Test : test_add_ingredient pass successfully")

    def test_add_wrong_ingredient(self):
        self.test_crate_household()
        ingredients_to_add = IngredientInput(
            ingredient_id=None,
            name="Banana",
            amount=-100,
            unit='gram'
        )
        response = add_ingredient_to_household(self.household_id, self.user_email, ingredients_to_add)
        self.assertEqual(400, response.status_code)
        ingredients_to_add.amount = 40
        ingredients_to_add.name = "a"
        response = add_ingredient_to_household(self.household_id, self.user_email, ingredients_to_add)
        self.assertEqual(404, response.status_code)
        logger.info(f"Test : test_add_wrong_ingredient pass successfully")

    def test_remove_user_from_household(self):
        self.test_crate_household()
        user = build_user_input()
        user.email = "ServerTest2@ServerTest2.ServerTest2"
        add_user(user)

        response = add_user_to_household(user.email, self.household_id)
        self.assertEqual(200, response.status_code)

        response = get_household_by_household_id_and_userEmail(self.user_email, self.household_id)
        household_users = response.json()['participants']
        self.assertIn(user.email, household_users)

        response = remove_user_from_household(user.email, self.household_id)
        self.assertEqual(200, response.status_code)

        response = get_household_by_household_id_and_userEmail(self.user_email, self.household_id)
        household_users = response.json()['participants']
        self.assertNotIn(user.email, household_users)

        delete_user(user.email)
        logger.info("Test : test_remove_user_from_household pass successfully")

    def test_remove_user_who_is_not_in_the_household(self):
        self.test_crate_household()
        response = remove_user_from_household("test@test.test", self.household_id)
        self.assertEqual(400, response.status_code)
        response = get_user(self.user_email)
        user_households = response.json()['households_ids']
        self.assertIn(self.household_id, user_households)
        response = get_household_by_household_id_and_userEmail(self.user_email, self.household_id)
        household_users = response.json()['participants']
        self.assertIn(self.user_email, household_users)

    def test_add_user_to_household(self):
        self.test_crate_household()
        user = build_user_input()
        user.email = "test@test.test"
        add_user(user)
        response = add_user_to_household(user.email, self.household_id)
        self.assertEqual(200, response.status_code)
        response = get_user(self.user_email)
        self.assertIn(self.household_id, response.json()['households_ids'])
        delete_user(user.email)
        logger.info("Test : test_add_user_to_household pass successfully")

    def test_add_wrong_user(self):
        self.test_crate_household()
        response = add_user_to_household("server_test", self.household_id)
        self.assertEqual(400, response.status_code)
        response = add_user_to_household("server_test@server_test.server_test", self.household_id)
        self.assertEqual(409, response.status_code)
        response = add_user_to_household("server_testserver_test@server_testserver_test.server_testserver_test", self.household_id)
        self.assertEqual(400, response.status_code)

    def test_use_recipe(self):
        self.test_crate_household_with_Ingredients()
        response = get_recipes(self.user_email, self.household_id)
        self.assertEqual(200, response.status_code)
        recipes: [RecipeBoundaryWithGasPollution] = []
        for recipe in response.json():
            recipes.append(parse_recipe(recipe))
        for recipe in recipes:
            meal_type = meal_types[random.randint(0, len(meal_types)-1)]
            response = use_recipe(
                [self.user_email],
                self.household_id,
                meal_type,
                random.randint(1, 5),
                str(recipe.recipe_id))
            if response.status_code == 200:
                response = get_user(self.user_email)
                self.assertEqual(200, response.status_code)
                user = parse_user_boundary(response.json())
                self.assertIsNotNone(
                    user.meals[datetime.now().strftime("%Y-%m-%d")][meal_type][str(recipe.recipe_id)])
                print(user.meals[datetime.now().strftime("%Y-%m-%d")][meal_type][str(recipe.recipe_id)].users)
                self.assertIn(self.user_email,user.meals[datetime.now().strftime("%Y-%m-%d")][meal_type][str(recipe.recipe_id)].users)
                response = get_household_by_household_id_and_userEmail(self.user_email, self.household_id)
                self.assertEqual(200, response.status_code)
                household = parse_household(response.json())
                self.assertIsNotNone(
                    household.meals[datetime.now().strftime("%Y-%m-%d")][meal_type][str(recipe.recipe_id)])

        logger.info(f"Test : test_use_recipe pass successfully")


if __name__ == '__main__':
    unittest.main()
