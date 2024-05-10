# Server
# RecipeRescue API

## Description

RecipeRescue API is a RESTful web service built with Python and FastAPI. It provides endpoints for searching recipes based on ingredients, retrieving recipes by ID, and managing users and households.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Starting the Server

To start the server, run the following command:

    ```bash
    uvicorn main:app --reload


Endpoints

Recipes

    GET /recipes/getRecipesByIngredients
        Retrieves list of RecipeBoundary based on provided ingredients.
        The recipes provided may contain ingredients that are not on the ingredients list.
        ingredients: Comma-separated list of ingredients.

    GET /recipes/getRecipesByIngredientsWithoutMissedIngredients
        Retrieves list of RecipeBoundary based on provided ingredients, excluding those with missed ingredients.
        ingredients: Comma-separated list of ingredients.

    GET /recipes/getRecipeByID/{recipe_id}
        Retrieves a RecipeBoundary by its ID.
        recipe_id: ID of the recipe.

    GET /recipes/getRecipesByName/{recipe_name}
        Returns a list of recipes in this form:
        {
            "recipe_id": int,
            "recipe_name": string,
            "ingredients": [],
            "image_url": string
        }
        recipe_name: Name of the recipe.

    GET /getRecipeInstructions/{recipe_id}
        Retrieves a list of recipe_instructionsBoundary by this Id
        recipe_id: ID of the recipe.

Ingredients

    GET /getAllSystemIngredients
     Retrieves a list of ingredients in this from:
      {
        "ingredient_id": String,
        "name": Name of the ingredient
      }
    
    GET /autocompleteIngredient
    Retrieves a list of ingredients whose prefix is ​​a partial_name in this from:
      {
        "ingredient_id": String,
        "name": Name of the ingredient
      }
    partial_name : String

Users and Household Operations

    POST /users_household/createNewHousehold
        Creates a new household.
        user_mail: Email of the user creating the household.
        household_name: Name of the household.

    POST /add_user
        Create new user in system
        user : UserInputForAddUser
        user_mail: Email of the user.

    GET /get_user
        Return UserBoundary by user mail

    GET /get_household_user_by_id
        Retuen a HouseholdBoundary by user mail and household id.
        user_mail: Email of the user.
        household_id : Id of household

    GET /get_household_user_by_name
        Return a list of HouseholdBoundary with this household_name.
        user_mail: Email of the user.
        household_name : Name of household

    POST /users_household/addUserToHousehold
        Adds a user to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.

    POST /add_ingredient_to_household_by_ingredient_name
        Adds a ingredient to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        ingredient: IngredientInput

    POST /add_list_ingredients_to_household
        Adds a ingredients to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        list_ingredients: ListIngredientsInput

    DELETE /remove_ingredient_from_household_by_date
        Remove ingredient in household on a specific date.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        list_ingredients: IngredientToRemoveByDateInput

    DELETE /remove_ingredient_from_household
        Remove ingredient in household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        list_ingredients: IngredientInput

    GET /get_all_ingredients_in_household
        Retrieves a list of IngredientBoundary in household.
        user_mail: Email of the user to add.
        household_id: Id of the household.

    POST /use_recipe_by_recipe_id
        Add to the history of consumption of meals at household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        meal : MealInput

    GET /get_meal_types
        Return list of meals types
        
Object Definitions

RecipeBoundary

Represents a recipe object returned by the API.

    recipe_id: Unique identifier for the recipe.
    recipe_name: Name of the recipe.
    ingredients: List of ingredients in the recipe, each represented by an IngredientBoundary object.
    image_url: URL of the image associated with the recipe.

recipe_instructionsBoundary

Represents a instructions of recipe object returned by the API.
    name: Name of the recipe.
    steps : list of steps objects

stepObject

    equipment: List of equipments needed to prepare the recipe : [String]
    ingredients: List of ingredients needed to prepare the recipe  : [String]
    length : Time to prepare the recipe : Int
    number : Step number : Int
    description : Description of what to do in this step : String
    
IngredientBoundary

Represents an ingredient object returned by the API.

    ingredient_id: Unique identifier for the ingredient.
    name: Name of the ingredient.
    amount: Amount of the ingredient.
    unit: Unit of measurement for the amount.
    purchase_date: Date the ingredient was purchased.

HouseholdBoundary

Represents a household object returned by the API.

    household_id: Unique identifier for the household.(String)
    household_name: Name of the household.(String)
    household_image: Image associated with the household.(String)
    participants: List of participants email in the household.(String)
    ingredients: Dictionary of ingredients in the household, where keys are ingredient names and values are lists of IngredientBoundary objects.
    meals: List of meals in the household, where keys are meal dates and values are meal types ("Breakfast", "Lunch", "Dinner", "Snacks"), the type is a dictionary of recipe ID and value is              MealBoundary.

MealBoundary

    type : "Breakfast" Or "Lunch" Or "Dinner" Or "Snakes". (String)
    users: list of users that take a part of this meal. ([String])
    recipe_id : id of recipe. (String)
    number_of_dishes : The number of dishes that will be made from the recipe in this meal.(Double)

UserBoundary

Represents a user object returned by the API.

    first_name: First name of the user.
    last_name: Last name of the user.
    user_email: Email of the user.
    image: Image associated with the user.
    households_ids: List of household IDs the user belongs to.
    meals: List of meals associated with the user, each represented by a RecipeBoundary object.
    country: Country of the user.
    state: State of the user.

UserInputForAddUser

    first_name: String
    last_name: String
    email: String
    country: String
    state: Optional[String]

IngredientInput

    IngredientName: The name of the ingredient. (String)
    IngredientAmount: The amount of the ingredient in grams. (Double)

ListIngredientsInput

    ingredients: [IngredientInput]

IngredientToRemoveByDateInput

    ingredient_data: IngredientInput
    year: int
    mount: int
    day: int

MealInput

    recipe_id: String
    meal_type: Must be one of them "Breakfast","Lunch" ,"Dinner","Snakes" String
    dishes_num: Double
    ingredients: [IngredientInput]
