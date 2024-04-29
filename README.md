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
        Retrieves recipes based on provided ingredients.
        ingredients: Comma-separated list of ingredients.

    GET /recipes/getRecipesByIngredientsWithoutMissedIngredients
        Retrieves recipes based on provided ingredients, excluding those with missed ingredients.
        ingredients: Comma-separated list of ingredients.

    GET /recipes/getRecipeByID/{recipe_id}
        Retrieves a recipe by its ID.
        recipe_id: ID of the recipe.

    GET /recipes/getRecipesByIDs
        Retrieves recipes by their IDs.
        recipe_ids: Comma-separated list of recipe IDs.

    GET /recipes/getRecipesByName/{recipe_name}
        Retrieves recipes by their names.
        recipe_name: Name of the recipe.

Users and Household Operations

    POST /users_household/createNewHousehold
        Creates a new household.
        user_mail: Email of the user creating the household.
        household_name: Name of the household.

    POST /users_household/addUserToHousehold
        Adds a user to an existing household.
        user_mail: Email of the user to add.
        household_name: Name of the household.

    DELETE /users_household/removeUserFromHousehold
        Removes a user from a household.
        user_mail: Email of the user to remove.
        household_name: Name of the household.

    GET /users_household/getUsersInHousehold
        Retrieves all users in a household.
        household_name: Name of the household.

Object Definitions
RecipeBoundary

Represents a recipe object returned by the API.

    id: Unique identifier for the recipe.
    recipe_name: Name of the recipe.
    ingredients: List of ingredients in the recipe, each represented by an IngredientBoundary object.
    image_url: URL of the image associated with the recipe.

IngredientBoundary

Represents an ingredient object returned by the API.

    ingredient_id: Unique identifier for the ingredient.
    name: Name of the ingredient.
    amount: Amount of the ingredient.
    unit: Unit of measurement for the amount.
    purchase_date: Date the ingredient was purchased.

HouseholdBoundary

Represents a household object returned by the API.

    household_id: Unique identifier for the household.
    household_name: Name of the household.
    household_image: Image associated with the household.
    participants: List of participants in the household.
    ingredients: Dictionary of ingredients in the household, where keys are ingredient names and values are lists of IngredientBoundary objects.
    meals: List of meals in the household, each represented by a RecipeBoundary object.

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
