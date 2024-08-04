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

    ```bash```
    uvicorn main:app --reload


Endpoints

#Recipes

# Recipe API

## `GET /recipes/getRecipesByIngredients`

This endpoint allows users to get a list of recipes based on a list of ingredients provided to the server.

### Parameters

- **`ingredients`**: A string representing the list of ingredients, separated by commas. Example: `Banana,avocado,pineapple,salt,soy,white bread,hummus,salmon,eggs,potato,oil,pepper`.

### Response

On success, the server returns a list of recipes matching the provided ingredients. Each recipe includes the following information:
- **`recipe_id`**: The unique identifier of the recipe.
- **`recipe_name`**: The name of the recipe.
- **`ingredients`**: A list of ingredients required for the recipe, including ID, name, amount, unit of measure, and purchase date (if available).
- **`image_url`**: A URL to an image of the recipe.
- **`sumGasPollution`**: The total gas pollution for the recipe, measured in CO2 units.

### Possible Errors

- **400 Bad Request**: Returned if the `ingredients` parameter is empty or improperly formatted.
- **404 Not Found**: Returned if no recipes match the provided ingredients or if an error occurs during recipe retrieval.
- **500 Internal Server Error**: Returned if there is a server-side error while processing the request.

### Example Response

```json
[
  {
    "recipe_id": 663338,
    "recipe_name": "The Scotch Egg",
    "ingredients": [
      {
        "ingredient_id": "1007063",
        "name": "pork sausage",
        "amount": 453.59,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "10018079",
        "name": "panko breadcrumbs",
        "amount": 120,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1123",
        "name": "eggs",
        "amount": 300,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/663338-312x231.jpg",
    "sumGasPollution": {
      "CO2": 4720.3017
    }
  },
  ...
]
```

## `GET /recipes/getRecipesByIngredientsWithoutMissingIngredients`

This endpoint allows users to get a list of recipes based on a list of ingredients provided to the server, ensuring that the recipes do not have missing ingredients.

### Parameters

- **`ingredients`**: A string representing the list of ingredients, separated by commas. Example: `Banana,avocado,pineapple,salt,soy sauce,white bread,hummus,salmon,eggs,potato,oil,pepper`.

### Response

On success, the server returns a list of recipes that do not have missing ingredients. Each recipe includes the following information:
- **`recipe_id`**: The unique identifier of the recipe.
- **`recipe_name`**: The name of the recipe.
- **`ingredients`**: A list of ingredients required for the recipe, including ID, name, amount, unit of measure, and purchase date (if available).
- **`image_url`**: A URL to an image of the recipe.
- **`sumGasPollution`**: The total gas pollution for the recipe, measured in CO2 units.

### Possible Errors

- **404 Not Found**: Returned if no recipes match the provided ingredients or if an error occurs during recipe retrieval.
- **500 Internal Server Error**: Returned if there is a server-side error while processing the request.

## `GET /recipes/getRecipeByID/{recipe_id}`

This endpoint allows users to retrieve detailed information about a specific recipe by its unique ID.

### Path Parameters

- **`recipe_id`**: The unique identifier of the recipe. Example: `660313`.

### Response

On success, the server returns detailed information about the recipe, including:
- **`recipe_id`**: The unique identifier of the recipe.
- **`recipe_name`**: The name of the recipe.
- **`ingredients`**: A list of ingredients required for the recipe, including:
  - **`ingredient_id`**: The unique identifier of the ingredient.
  - **`name`**: The name of the ingredient.
  - **`amount`**: The amount of the ingredient.
  - **`unit`**: The unit of measure for the ingredient.
  - **`purchase_date`**: The date when the ingredient was purchased (if available).
- **`image_url`**: A URL to an image of the recipe.
- **`sumGasPollution`**: The total gas pollution for the recipe, measured in CO2 units.

### Possible Errors

- **404 Not Found**: Returned if the `recipe_id` does not exist or if an error occurs during recipe retrieval.
- **500 Internal Server Error**: Returned if there is a server-side error while processing the request.

## `GET /recipes/getRecipesByName/{recipe_name}`

This endpoint allows users to retrieve a list of recipes that match a specific name.

### Path Parameters

- **`recipe_name`**: The name of the recipe to search for. This parameter should be URL-encoded if it contains special characters or spaces. Example: `Slow-Roasted%20Tomatoes`.

### Response

On success, the server returns a list of recipes that match the provided name. Each recipe includes:
- **`recipe_id`**: The unique identifier of the recipe.
- **`recipe_name`**: The name of the recipe.
- **`ingredients`**: A list of ingredients required for the recipe, including:
  - **`ingredient_id`**: The unique identifier of the ingredient.
  - **`name`**: The name of the ingredient.
  - **`amount`**: The amount of the ingredient.
  - **`unit`**: The unit of measure for the ingredient.
  - **`purchase_date`**: The date when the ingredient was purchased (if available).
- **`image_url`**: A URL to an image of the recipe.
- **`sumGasPollution`**: The total gas pollution for the recipe, measured in CO2 units.

### Possible Errors

- **404 Not Found**: Returned if no recipes are found for the provided name or if an error occurs during recipe retrieval.
- **500 Internal Server Error**: Returned if there is a server-side error while processing the request.

## `GET /recipes/getRecipeInstructions/{recipe_id}`

This endpoint allows users to retrieve the cooking instructions for a specific recipe based on its unique ID.

### Path Parameters

- **`recipe_id`**: The unique identifier of the recipe for which you want to retrieve instructions.

### Response

On success, the server returns the cooking instructions for the specified recipe. The response includes:
- **`name`**: The name of the recipe (if available).
- **`steps`**: A list of steps for preparing the recipe. Each step includes:
  - **`number`**: The step number.
  - **`description`**: The detailed description of the step.
  - **`length`**: The duration of the step in seconds (if applicable).
  - **`equipment`**: A list of equipment used in this step, with image URLs.
  - **`ingredients`**: A list of ingredients used in this step, with image URLs.
- **`total_length`**: The total length of all steps in seconds.

### Possible Errors

- **400 Bad Request**: Returned if there is an error while retrieving the instructions for the specified recipe.

```json
{
  "name": "",
  "steps": [
    {
      "equipment": [
        {
          "oven": "https://spoonacular.com/cdn/equipment_100x100/oven.jpg"
        }
      ],
      "ingredients": [],
      "length": 0,
      "number": 1,
      "description": "Preheat oven to 150 C or 280 F"
    },
    {
      "equipment": [],
      "ingredients": [
        {
          "tomato": "tomato.png"
        }
      ],
      "length": 0,
      "number": 2,
      "description": "Cut the top 3rd off the tomatoes & discard top."
    },
    {
      "equipment": [
        {
          "baking paper": "https://spoonacular.com/cdn/equipment_100x100/baking-paper.jpg"
        },
        {
          "baking pan": "https://spoonacular.com/cdn/equipment_100x100/roasting-pan.jpg"
        }
      ],
      "ingredients": [
        {
          "tomato": "tomato.png"
        }
      ],
      "length": 0,
      "number": 3,
      "description": "Place tomatoes on a baking tray, lined with parchment paper."
    },
    {
      "equipment": [],
      "ingredients": [
        {
          "pepper": "pepper.jpg"
        },
        {
          "herbs": "mixed-fresh-herbs.jpg"
        },
        {
          "salt": "salt.jpg"
        }
      ],
      "length": 0,
      "number": 4,
      "description": "Sprinkle generously with salt, pepper & herbs."
    },
    {
      "equipment": [],
      "ingredients": [
        {
          "olive oil": "olive-oil.jpg"
        }
      ],
      "length": 0,
      "number": 5,
      "description": "Drizzle with a generous amount of olive oil."
    },
    {
      "equipment": [
        {
          "oven": "https://spoonacular.com/cdn/equipment_100x100/oven.jpg"
        },
        {
          "frying pan": "https://spoonacular.com/cdn/equipment_100x100/pan.png"
        }
      ],
      "ingredients": [
        {
          "olive oil": "olive-oil.jpg"
        },
        {
          "tomato": "tomato.png"
        }
      ],
      "length": 360,
      "number": 6,
      "description": "Place in the oven for 4-6 hours depending on the size of your tomatoes. Every once in a while as you pass the kitchen, baste the tomatoes in the juices & olive oil in the pan."
    },
    {
      "equipment": [],
      "ingredients": [
        {
          "tomato": "tomato.png"
        }
      ],
      "length": 0,
      "number": 7,
      "description": "Once the tomatoes shrivel up a bit & start to look sun-dried, they are ready. They should still hold their shape & not become mush."
    },
    {
      "equipment": [
        {
          "oven": "https://spoonacular.com/cdn/equipment_100x100/oven.jpg"
        }
      ],
      "ingredients": [
        {
          "anchovies": "anchovies.jpg"
        },
        {
          "tomato": "tomato.png"
        }
      ],
      "length": 0,
      "number": 8,
      "description": "Remove from oven, top each tomato with a whole anchovy filet."
    },
    {
      "equipment": [
        {
          "baking pan": "https://spoonacular.com/cdn/equipment_100x100/roasting-pan.jpg"
        }
      ],
      "ingredients": [
        {
          "olive oil": "olive-oil.jpg"
        }
      ],
      "length": 0,
      "number": 9,
      "description": "Serve warm or room temperature with olive oil from the baking pan drizzled over the top."
    }
  ],
  "total_length": 360
}
```


#Ingredients API

## `GET /ingredients/getAllSystemIngredients`

Retrieves all food ingredients that exist in the system.

### Response

- **200 OK**: Returns a list of all ingredients in the system.
  - **`ingredient_id`**: Unique identifier of the ingredient.
  - **`name`**: Name of the ingredient.
  - **`days_to_expire`**: Number of days until the ingredient expires.
  - **`gCO2e_per_100g`**: CO2 emissions per 100 grams of the ingredient.
```json
[
  {
    "ingredient_id": "20081",
    "name": "flour",
    "days_to_expire": 365,
    "gCO2e_per_100g": 89
  },
  {
    "ingredient_id": "14412",
    "name": "water",
    "days_to_expire": 30,
    "gCO2e_per_100g": 32
  },
  {
    "ingredient_id": "11282",
    "name": "onion",
    "days_to_expire": 30,
    "gCO2e_per_100g": 231
  },
  {
    "ingredient_id": "1082047",
    "name": "kosher salt",
    "days_to_expire": 3650,
    "gCO2e_per_100g": 50
  }
]
```

## `GET /ingredients/getIngredientById`

Retrieves a specific ingredient from the system by its unique identifier.

### Parameters

- **`ingredient_id`** (query parameter): The unique identifier of the ingredient.

### Response

- **200 OK**: Returns details of the specified ingredient.
  - **`ingredient_id`**: Unique identifier of the ingredient.
  - **`name`**: Name of the ingredient.
  - **`days_to_expire`**: Number of days until the ingredient expires.
  - **`gCO2e_per_100g`**: CO2 emissions per 100 grams of the ingredient.
    
## `GET /ingredients/getIngredientByName`

Retrieves a specific ingredient from the system by its name.

### Parameters

- **`ingredient_name`** (query parameter): The name of the ingredient to search for.

### Response

- **200 OK**: Returns details of the specified ingredient.
  - **`ingredient_id`**: Unique identifier of the ingredient.
  - **`name`**: Name of the ingredient.
  - **`days_to_expire`**: Number of days until the ingredient expires.
  - **`gCO2e_per_100g`**: CO2 emissions per 100 grams of the ingredient.

#Users and Household API

## `POST /usersAndHouseholdManagement/createNewHousehold`

**Description:**
This endpoint allows users to create a new household and optionally add ingredients to it. The household is created based on the user's email and a given household name. If ingredients are provided, they will be added to the newly created household.

- **Query Parameters:**
- `user_email` (required): The email address of the user creating the household.
- `household_name` (required): The name of the new household.

- **Body Parameters:**
- `ingredients` (optional): A list of ingredients to add to the household. Each ingredient includes:
  - `ingredient_id` (string, optional): The ID of the ingredient (can be omitted if not needed).
  - `name` (string): The name of the ingredient.
  - `amount` (number): The amount of the ingredient.
  - `unit` (string): The unit of measurement for the ingredient.
### Response

- **200 OK**: The household was created successfully and optionally, ingredients were added.
  - ```json
    {
      "message": "Household added successfully",
      "household_id": "3efe25e8-4272-4cfd-9524-fc391ad9b70f"
    }
    ```
- **404 No Found**: The user could not be found.
- **400 Bad Request**: Invalid arguments or data provided in the request.
- ```josn
  {
      "detail": "Error message describing what went wrong"
  }
    ```

## `DELETE /usersAndHouseholdManagement/deleteHousehold`

**Description:**
This endpoint allows users to delete a household by its ID. The specified household is removed from the system.
- **Query Parameters:**
- `household_id` (required): The unique identifier of the household to be deleted.
**Response:**
- **Status Codes:**
  - `200 OK`: The household was successfully deleted.
  - `404 Not Found`: The household with the specified ID was not found or could not be deleted.

## `POST /usersAndHouseholdManagement/addUser`

This endpoint is used to add a new user to the system.

**Request Body:**

The request should contain a JSON object with the following fields:

- `first_name` (string): The first name of the user.
- `last_name` (string): The last name of the user.
- `email` (string): The email address of the user. Must be unique.
- `country` (string): The country where the user resides.
- `state` (string): The state or province where the user resides.

**Response:**

- **Status Codes:**
  - `200 OK`: Successfully added the user.
  - ```json
    {
      "message": "Successfully Added User example@example.example"
    }
    ```
  - `409 Conflict`: The email address provided already exists or there was a conflict in creating the user.
  - `400 Bad Request`: There was an issue with the input data.


## `GET /usersAndHouseholdManagement/getUser`

Retrieves a user by their email address.

**Query Parameters:**
- `user_email` (string): The email address of the user to retrieve.

**Response:**

- **Status Codes:**
  - `200 OK`: The user was successfully retrieved.
  - ```json
        {
          "first_name": "example",
          "last_name": "example",
          "user_email": "example@example.example",
          "image": null,
          "households_ids": [],
          "meals": {},
          "country": "example",
          "state": "example",
          "sum_gas_pollution": {
            "CO2": 0
          }
        }
    ```
  - `404`: 
  ```json
      {
          "detail": "User does not exist"
        }
  ```
  - `400 Bad Request`: There was an issue with the input data.
  - ```json
    {
      "detail": "example@.example invalid email format"
    }
    ```
## `GET /usersAndHouseholdManagement/getAllHouseholdsByUserEmail`

Retrieves all households associated with a specific user by their email address.

**Query Parameters:**
- `user_email` (string): The email address of the user whose households are to be retrieved.

**Response:**

- **Status Codes:**
  - `200 OK`: Successfully retrieved all households for the user.
```json
{
  "67fc717d-67b4-43e0-a8dc-cb5189a9c383": {
    "household_id": "67fc717d-67b4-43e0-a8dc-cb5189a9c383",
    "household_name": "server_test",
    "participants": [
      {
        "first_name": "Nissan",
        "last_name": "Yamin",
        "user_email": "nissanyam1@gmail.com",
        "sum_gas_pollution": {
          "CO2": 59064.59
        }
      },
      {
        "first_name": "Linoy",
        "last_name": "Penikar",
        "user_email": "linoy@gmail.com",
        "sum_gas_pollution": {
          "CO2": 6752.25
        }
      }
    ],
    "ingredients": {
      "1001": [
        {
          "name": "butter",
          "amount": 5555345,
          "unit": "gram",
          "expiration_date": "2024-07-23"
        }
      ],
      "1033": [
        {
          "name": "parmesan cheese",
          "amount": 12089.00,
          "unit": "gram",
          "expiration_date": "2024-07-10"
        }
      ],
      // Additional ingredients omitted for brevity
    },
    "meals": {
      "2024-08-02": {
        "Lunch": {
          "640089": [
            {
              "users": ["nissanyam1@gmail.com"],
              "number_of_dishes": 1,
              "sum_gas_pollution": {
                "CO2": 1110.1
              }
            },
            {
              "users": ["nissanyam1@gmail.com", "linoy@gmail.com"],
              "number_of_dishes": 2,
              "sum_gas_pollution": {
                "CO2": 2220.2
              }
            }
          ]
        }
      }
    },
    "sum_gas_pollution": {
      "CO2": 3330.30
    }
  }
}
```
  - `400 Bad Request`: The provided email has an invalid format.
  - `404 Not Found`: The user with the specified email does not exist.

## `PUT /usersAndHouseholdManagement/updatePersonalUserInfo`

**Request Body Example:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "country": "string",
  "state": "string"
}

**Response:**

- **Status Codes:**
  - `200 OK`: User information updated successfully.
  - `400 Bad Request`: Invalid input data (e.g., invalid email format).
  - `404 Not Found`: User with the specified email does not exist.


## `DELETE /usersAndHouseholdManagement/deleteUser`

**Description:**

Deletes a user by their email address.

**Request:**

- **Query Parameter:**
  - `user_email` (string): The email address of the user to be deleted.

**Response:**

- **Status Codes:**
  - `200 OK`: User deleted successfully.
  - `404 Not Found`: User with the specified email does not exist or could not be deleted.


## `GET /usersAndHouseholdManagement/getHouseholdUserById`

**Description:**

Retrieves information about a specific household by its ID for a given user email.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user.
  - `household_id` (string): The ID of the household.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "household_id": "67fc717d-67b4-43e0-a8dc-cb5189a9c383",
      "household_name": "server_test",
      "household_image": null,
      "participants": [
        "nissanyam1@gmail.com",
        "linoy@gmail.com"
      ],
      "ingredients": {
        "1001": [
          {
            "ingredient_id": "1001",
            "name": "butter",
            "amount": 5555345,
            "unit": "gram",
            "purchase_date": "2024-07-09",
            "expiration_date": "2024-07-23"
          }
        ],
        ...
      },
      "meals": {
        "2024-06-26": {
          "Breakfast": {
            "642582": [
              {
                "users": [
                  "server_test@server_test.server_test"
                ],
                "number_of_dishes": 4,
                "sum_gas_pollution": {
                  "CO2": 3906.29
                }
              },
              ...
            ]
          }
        }
      },
      "sum_gas_pollution": {
        "CO2": 84272.08
      }
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid request parameters."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Household does not exist."
    }
    ```


## `GET /usersAndHouseholdManagement/getHouseholdAndUsersDataById`

**Description:**

Retrieves detailed information about a specific household and its users by household ID for a given user email.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user.
  - `household_id` (string): The ID of the household.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "household_id": "67fc717d-67b4-43e0-a8dc-cb5189a9c383",
      "household_name": "server_test",
      "household_image": null,
      "participants": [
        {
          "first_name": "Nissan",
          "last_name": "Yamin",
          "user_email": "nissanyam1@gmail.com",
          "image": null,
          "country": "Israel",
          "state": "Haifa District",
          "sum_gas_pollution": {
            "CO2": 59064.59
          }
        },
        {
          "first_name": "Linoy",
          "last_name": "Penikar",
          "user_email": "linoy@gmail.com",
          "image": null,
          "country": "Israel",
          "state": "Haifa",
          "sum_gas_pollution": {
            "CO2": 6752.25
          }
        }
      ],
      "ingredients": {
        "1001": [
          {
            "ingredient_id": "1001",
            "name": "butter",
            "amount": 5555345,
            "unit": "gram",
            "purchase_date": "2024-07-09",
            "expiration_date": "2024-07-23"
          }
        ],
        ...
      },
      "meals": {
        "2024-06-26": {
          "Breakfast": {
            "642582": [
              {
                "users": [
                  "server_test@server_test.server_test"
                ],
                "number_of_dishes": 4,
                "sum_gas_pollution": {
                  "CO2": 3906.29
                }
              },
              ...
            ]
          }
        }
      },
      "sum_gas_pollution": {
        "CO2": 84272.08
      }
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid request parameters."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Household or user does not exist."
    }
    ```

## `GET /usersAndHouseholdManagement/getHouseholdUserByName`

**Description:**

Retrieves information about households and their users based on the household name for a specific user email.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user requesting the information.
  - `household_name` (string): The name of the household.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid request parameters."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Household or user does not exist."
    }
    ```

## `POST /usersAndHouseholdManagement/addUserToHousehold`

**Description:**

Adds a user to a specified household.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user to be added.
  - `household_id` (string): The ID of the household to which the user is to be added.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "message": "User '{user_email}' added to household '{household_id}' successfully."
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid input data or request parameters."
    }
    ```
  - **Status Code: `409 Conflict`**
    ```json
    {
      "detail": "Conflict occurred while adding user to household."
    }
    ```

## `DELETE /usersAndHouseholdManagement/removeUserFromHousehold`

**Description:**

Removes a user from a specified household.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user to be removed.
  - `household_id` (string): The ID of the household from which the user is to be removed.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "message": "User '{user_email}' removed from household '{household_id}' successfully."
    }
    ```

- **Error Response:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid input data or request parameters."
    }
    ```


## `POST /usersAndHouseholdManagement/addIngredientToHouseholdByIngredientName`

**Description:**

Adds an ingredient to a specified household using the ingredient's name.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user adding the ingredient.
  - `household_id` (string): The ID of the household to which the ingredient is to be added.
  
- **Body:**
  - `IngredientInput` (object):
    - `name` (string): The name of the ingredient.
    - `amount` (number): The amount of the ingredient.
    - `unit` (string): The unit of measurement for the ingredient.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "message": "Ingredient '{ingredient.name}' added to household '{household_id}' successfully by user '{user_email}'."
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid input data or request parameters."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Ingredient does not exist or household not found."
    }
    ```


## `POST /usersAndHouseholdManagement/updateIngredientInHousehold`

**Description:**

Updates an ingredient in a specified household based on the provided date.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user making the update.
  - `household_id` (string): The ID of the household where the ingredient is to be updated.
  
- **Body:**
  - `IngredientToRemoveByDateInput` (object):
    - `ingredient_data` (object):
      - `name` (string): The name of the ingredient.
      - `amount` (number): The new amount of the ingredient.
    - `date` (object):
      - `year` (number): The year of the date.
      - `month` (number): The month of the date.
      - `day` (number): The day of the date.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "message": "Ingredient '{ingredient.name}' in {ingredient_date} from household '{household_id}' updated successfully by user '{user_email}'."
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Provided date cannot be later than today or invalid date provided."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Error updating ingredient in household."
    }
    ```

## `POST /usersAndHouseholdManagement/addListIngredientsToHousehold`

**Description:**

Adds a list of ingredients to a specified household.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user making the request.
  - `household_id` (string): The ID of the household where the ingredients are to be added.

- **Body:**
  - `ListIngredientsInput` (object):
    - `ingredients` (array of objects):
      - `name` (string): The name of the ingredient.
      - `amount` (number): The amount of the ingredient.
      - `unit` (string): The unit of measurement for the ingredient.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "message": "List of ingredients added to household '{household_id}' successfully by user '{user_email}'."
    }
    ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid input data."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Household or user not found."
    }
    ```

## `DELETE /usersAndHouseholdManagement/removeIngredientFromHouseholdByDate`

**Description:**

Removes an ingredient from a specified household based on the given date.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user making the request.
  - `household_id` (string): The ID of the household from which the ingredient is to be removed.

- **Body:**
  - `IngredientToRemoveByDateInput` (object):
    - `ingredient_data` (object):
      - `name` (string): The name of the ingredient.
      - `amount` (number): The amount of the ingredient.
    - `date` (object):
      - `year` (number): The year of the date.
      - `month` (number): The month of the date.
      - `day` (number): The day of the date.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Invalid date provided."
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Error removing ingredient {ingredient.ingredient_data.name} from household: {household_id} in date {ingredient_date}."
    }
    ```
### `DELETE /usersAndHouseholdManagement/removeIngredientFromHousehold`

**Description:**

Removes a specified ingredient from a household.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user making the request.
  - `household_id` (string): The ID of the household from which the ingredient is to be removed.

- **Body:**
  - `IngredientInput` (object):
    - `name` (string): The name of the ingredient.
    - `amount` (number): The amount of the ingredient.
    - `ingredient_id` (string): The ID of the ingredient.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
- **Error Responses:**
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Error removing ingredient {ingredient.ingredient_id} : {ingredient.name} from household '{household_id}': {e}"
    }
    ```
    or
    ```json
    {
      "detail": "Invalid argument error removing ingredient {ingredient.ingredient_id} : {ingredient.name} from household '{household_id}': {e.message}"
    }
    ```

### `GET /usersAndHouseholdManagement/getAllIngredientsInHousehold`

**Description:**

Retrieves all ingredients from a specified household.

**Request:**

- **Query Parameters:**
  - `user_email` (string): The email address of the user making the request.
  - `household_id` (string): The ID of the household from which ingredients are to be retrieved.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    ```json
    {
      "ingredients": [
        {
          "ingredient_id": "string",
          "name": "string",
          "amount": number,
          "unit": "string",
          "purchase_date": "YYYY-MM-DD",
          "expiration_date": "YYYY-MM-DD"
        }
        //... additional ingredients
      ]
    }
    ```
    - Example:
      ```json
      {
        "ingredients": [
          {
            "ingredient_id": "1001",
            "name": "butter",
            "amount": 5555345,
            "unit": "gram",
            "purchase_date": "2024-07-09",
            "expiration_date": "2024-07-23"
          },
          {
            "ingredient_id": "1033",
            "name": "parmesan cheese",
            "amount": 12089.000000000004,
            "unit": "gram",
            "purchase_date": "2024-06-26",
            "expiration_date": "2024-07-10"
          }
          //... additional ingredients
        ]
      }
      ```

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    ```json
    {
      "detail": "Error retrieving all ingredients from household: {e.message}"
    }
    ```
  - **Status Code: `404 Not Found`**
    ```json
    {
      "detail": "Error retrieving all ingredients from household: {e.message}"
    }
    ```

## `POST /useRecipeByRecipeId`

**Description:**

Uses a specified recipe for a given number of dishes in a household.

**Parameters:**

- `users_email` (List[str]): List of user emails.
- `household_id` (string): The household ID.
- `meal` (string): The meal type.
- `dishes_num` (float): The number of dishes.
- `recipe_id` (string): The recipe ID.

**Response:**

- **Success Response:**
  - **Status Code: `200 OK`**
    - No content is returned on success.

- **Error Responses:**
  - **Status Code: `400 Bad Request`**
    - Invalid meal type.
    - Dishes number should be greater than 0.
    - Value error while using recipe.
    - Unexpected error while using recipe.
  - **Status Code: `404 Not Found`**


##GET /getMealTypes`

### Description

Retrieves the list of meal types.

### Request

This endpoint does not require any parameters.

### Response

- **Status Code**: `200 OK`
- **Body**: A list of meal types.



## getAllRecipesThatHouseholdCanMake

### Endpoint

`GET /getAllRecipesThatHouseholdCanMake`

### Description

Retrieves all recipes that a household can make based on the ingredients available, considering CO2 emissions and expiration dates of ingredients.

### Request

#### Parameters

- `user_email` (str): The email of the user requesting the recipes.
- `household_id` (str): The ID of the household for which recipes are being requested.
- `co2_weight` (float, optional): The weight given to CO2 emissions in the sorting of recipes (default: 0.5).
- `expiration_weight` (float, optional): The weight given to the expiration date of ingredients in the sorting of recipes (default: 0.5).

#### Example Request

### Response

- **Status Code**: `200 OK`
- **Body**: A list of recipes that the household can make, sorted by a composite score based on CO2 emissions and expiration dates.

#### Example Response

```json
[
  {
    "recipe_id": 640089,
    "recipe_name": "Corn on the Cob in Cilantro and Lime Butter",
    "ingredients": [
      {
        "ingredient_id": "1001",
        "name": "butter",
        "amount": 113,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11165",
        "name": "cilantro",
        "amount": 4,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "9159",
        "name": "lime",
        "amount": 6,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11167",
        "name": "corn on the cob",
        "amount": 3,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/640089-312x231.jpg",
    "sumGasPollution": {
      "CO2": 1110.1
    },
    "closest_expiration_days": 2
  },
  {
    "recipe_id": 642582,
    "recipe_name": "Farfalle With Broccoli, Carrots and Tomatoes",
    "ingredients": [
      {
        "ingredient_id": "10120420",
        "name": "farfalle pasta",
        "amount": 453.59,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11124",
        "name": "carrots",
        "amount": 3,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11090",
        "name": "broccoli heads",
        "amount": 5.08,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11291",
        "name": "scallions",
        "amount": 48,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "10211215",
        "name": "garlic cloves",
        "amount": 3,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1033",
        "name": "parmigiano-reggiano",
        "amount": 100,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "10111529",
        "name": "grape tomatoes",
        "amount": 226,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/642582-312x231.jpg",
    "sumGasPollution": {
      "CO2": 976.5714
    },
    "closest_expiration_days": 13
  },
  {
    "recipe_id": 642138,
    "recipe_name": "Easy Vegetable Fried Rice",
    "ingredients": [
      {
        "ingredient_id": "11090",
        "name": "broccoli",
        "amount": 88,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1001",
        "name": "butter",
        "amount": 14.2,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11124",
        "name": "carrots",
        "amount": 42.67,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "10220445",
        "name": "rice",
        "amount": 370,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1123",
        "name": "egg",
        "amount": 1,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11215",
        "name": "garlic",
        "amount": 3,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11216",
        "name": "ginger",
        "amount": 7,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11052",
        "name": "green beans",
        "amount": 55,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11304",
        "name": "peas",
        "amount": 72.5,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "16124",
        "name": "soy sauce",
        "amount": 72,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/642138-312x231.jpg",
    "sumGasPollution": {
      "CO2": 671.6101
    },
    "closest_expiration_days": 13
  },
  {
    "recipe_id": 652966,
    "recipe_name": "Nasturtium Pesto",
    "ingredients": [
      {
        "ingredient_id": "2004",
        "name": "nasturtium flowers and leaves",
        "amount": 473.18,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11677",
        "name": "shallot",
        "amount": 10,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11215",
        "name": "garlic",
        "amount": 3,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "12155",
        "name": "walnuts",
        "amount": 58.5,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/652966-312x231.jpg",
    "sumGasPollution": {
      "CO2": 575.7934
    },
    "closest_expiration_days": 29
  },
  {
    "recipe_id": 643514,
    "recipe_name": "Fresh Herb Omelette",
    "ingredients": [
      {
        "ingredient_id": "2044",
        "name": "basil",
        "amount": 2,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1123",
        "name": "eggs",
        "amount": 2,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "11291",
        "name": "green onion",
        "amount": 12.5,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "10311529",
        "name": "cherry tomatoes",
        "amount": 4,
        "unit": "gram",
        "purchase_date": null
      },
      {
        "ingredient_id": "1033",
        "name": "parmesan cheese",
        "amount": 12.5,
        "unit": "gram",
        "purchase_date": null
      }
    ],
    "image_url": "https://img.spoonacular.com/recipes/643514-312x231.jpg",
    "sumGasPollution": {
      "CO2": 94.53
    },
    "closest_expiration_days": 13
  }
]


## `GET /checkIfHouseholdExistInSystem`

### Description
Checks if a household with a given ID exists in the system.

### Parameters

- **Query Parameter**:
  - `household_id` (string): The unique identifier of the household to check.

### Responses

- **200 OK**:
  - Returns `true` if the household exists in the system.

- **404 Not Found**:
  - Returns an error message if the household does not exist in the system.

### Example Request

```http
GET /checkIfHouseholdExistInSystem?household_id=12345

## `GET /checkIfHouseholdCanMakeRecipe`

### Description
Checks if a household can make a specific recipe given the number of dishes.

### Parameters

- **Query Parameters**:
  - `household_id` (string): The unique identifier of the household.
  - `recipe_id` (string): The unique identifier of the recipe.
  - `dishes_num` (optional, float): The number of dishes to be prepared. Defaults to 1.

### Responses

- **200 OK**:
  - Returns a JSON object indicating whether the household can make the recipe.

- **400 Bad Request**:
  - Returns an error message if there is an issue with the request or the provided data.

### Example Request

```http
GET /checkIfHouseholdCanMakeRecipe?household_id=12345&recipe_id=67890&dishes_num=3



## `POST /getGasPollutionOfHouseholdInRangeDates`

### Description
Retrieves the gas pollution data for a specific household within a given date range.

### Parameters

- **Query Parameters**:
  - `user_email` (string): The email address of the user making the request.
  - `household_id` (string): The unique identifier of the household.
  - `startDate` (Date): The start date of the range for which to retrieve gas pollution data.
  - `endDate` (Date): The end date of the range for which to retrieve gas pollution data.

### Responses

- **200 OK**:
  - Returns the gas pollution data for the specified household and date range.

- **400 Bad Request**:
  - Returns an error message if there are issues with the dates or other request parameters.

### Example Request
```json
{
  "total_gas_pollution": 789.12
}
```
```http
POST /getGasPollutionOfHouseholdInRangeDates
Content-Type: application/json

{
  "user_email": "user@example.com",
  "household_id": "12345",
  "startDate": "2024-01-01",
  "endDate": "2024-01-31"
}

## `POST /getGasPollutionOfUserInRangeDates`

### Description
Retrieves the gas pollution data for a user within a specified date range.

### Parameters

- **Query Parameters**:
  - `user_email` (string): The email address of the user making the request.
  - `startDate` (Date): The start date of the range for which to retrieve gas pollution data.
  - `endDate` (Date): The end date of the range for which to retrieve gas pollution data.

### Responses

- **200 OK**:
  - Returns the gas pollution data for the specified user and date range.

- **400 Bad Request**:
  - Returned when the start date is not before the end date, or if invalid dates are provided.

- **404 Not Found**:
  - Returned if there are other issues processing the request.

### Example Request

```http
POST /getGasPollutionOfUserInRangeDates
Content-Type: application/json

{
  "user_email": "user@example.com",
  "startDate": "2024-01-01",
  "endDate": "2024-01-31"
}
```json
{
  "total_gas_pollution": 789.12
}
```


