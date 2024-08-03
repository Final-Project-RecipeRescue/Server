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

updatePersonalUserInfo 

      PUT /usersAndHouseholdManagement/updatePersonalUserInfo
      Update personal user information
      {
        "first_name": optional[string],
        "last_name": optional[string],
        "email": string - must be a valid email and existing user,
        "country": optional[string],
        "state": optional[string]
      }
      
deleteUser

    DELETE /usersAndHouseholdManagement/deleteUser
        Remove user from system and remove him from households
        user_mail: Email of the user

getHouseholdUserById

    GET /usersAndHouseholdManagement/getHouseholdUserById
        Retuen a HouseholdBoundary by user mail and household id.
        user_mail: Email of the user.
        household_id : Id of household
    Example:
    http://127.0.0.1:8000/usersAndHouseholdManagement/getHouseholdUserById?user_email=example%40example.example&household_id=2f249d7a-bca5-4ae1-87e3-cf3cba2b02b3
      
      Return value
      {
        "household_id": "2f249d7a-bca5-4ae1-87e3-cf3cba2b02b3",
        "household_name": "example",
        "household_image": null,
        "participants": [
          "example@example.example"
        ],
        "ingredients": {
          "1033": [
            {
              "ingredient_id": "1033",
              "name": "Parmesan cheese",
              "amonth": 1971.6599999999999,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "2044": [
            {
              "ingredient_id": "2044",
              "name": "Basil",
              "amonth": 952,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "2047": [
            {
              "ingredient_id": "2047",
              "name": "Salt",
              "amonth": 1000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "4053": [
            {
              "ingredient_id": "4053",
              "name": "Olive oil",
              "amonth": 1000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "5062": [
            {
              "ingredient_id": "5062",
              "name": "Chicken breast",
              "amonth": 2000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "11165": [
            {
              "ingredient_id": "11165",
              "name": "Cilantro",
              "amonth": 1000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "11215": [
            {
              "ingredient_id": "11215",
              "name": "Garlic",
              "amonth": 1000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "11216": [
            {
              "ingredient_id": "11216",
              "name": "Ginger",
              "amonth": 2000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
          "11529": [
            {
              "ingredient_id": "11529",
              "name": "Tomato",
              "amonth": 1000,
              "unit": "gram",
              "purchase_date": "2024-05-19"
            }
          ],
        },
        "meals": {
          "2024-05-19": {
            "Lunch": {
              "634435": [
                {
                  "users": [
                    "example@example.example"
                  ],
                  "number_of_dishes": 1
                },
                {
                  "users": [
                    "example@example.example"
                  ],
                  "number_of_dishes": 1
                }
              ]
            }
          }
        }
      }

getHouseholdAndUsersDataById

      GET /usersAndHouseholdManagement/getHouseholdAndUsersDataById
      Retuen a HouseholdBoundary by user mail and household id .
      The information in participants is not users' emails, it is users' objects.
         user_mail: Email of the user.
         household_id : Id of household

getHouseholdUserByName

    GET /usersAndHouseholdManagement/getHouseholdUserByName
        Return a list of HouseholdBoundary with this household_name.
        user_mail: Email of the user.
        household_name : Name of household

get_all_household_details_by_user_mail

    GET /usersAndHouseholdManagement/get_all_household_details_by_user_mail
        Detailed information about the user's households, including a list of each household's available ingredients. 
        Return a list of HouseholdBoundary or Null if there is a problem with the user's email 
        user_mail: Email of the user.

addUserToHousehold

    POST /usersAndHouseholdManagement/usersAndHouseholdManagement/addUserToHousehold
        Adds a user to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.

removeUserFromHousehold

      Delete /usersAndHouseholdManagement/removeUserFromHousehold
         Remove user from household
         user_mail: Email of the user to add.
         household_id: Id of the household.

addIngredientToHouseholdByIngredientName

    POST /usersAndHouseholdManagement/addIngredientToHouseholdByIngredientName
        Adds a ingredient to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        
         body:
            {
              "ingredient_id": Optional - "string",
              "name": "string",
              "amonth": greater than 0,
              "unit": Optional - "string"
            }

addListIngredientsToHousehold

    POST /usersAndHouseholdManagement/addListIngredientsToHousehold
        Adds a ingredients to an existing household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        list_ingredients: ListIngredientsInput

removeIngredientFromHouseholdByDate

    DELETE /usersAndHouseholdManagement/removeIngredientFromHouseholdByDate
        Remove ingredient in household on a specific date.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        ingredient : IngredientToRemoveByDateInput
         body example :
            {
              "ingredient_data": {
                "ingredient_id": "1001",
                "name": "Butter",
                "amonth": 3,
                "unit": "string"/// in defult in gram
              },
               "date":{
                 "year": 2024,
                 "month": 5,
                 "day": 19
               }

         }

removeIngredientFromHousehold

    DELETE /usersAndHouseholdManagement/removeIngredientFromHousehold
        Remove ingredient in household.
        user_mail: Email of the user to add.
        household_id: Id of the household.
        ingredient: IngredientInput
       body eample:
         {
           "ingredient_id": "string",
           "name": "string",
           "amonth": 0,
           "unit": "string"
         }

getAllIngredientsInHousehold

    GET /usersAndHouseholdManagement/getAllIngredientsInHousehold
        Retrieves a list of IngredientBoundary in household.
        user_mail: Email of the user to add.
        household_id: Id of the household.

useRecipeByRecipeId

    POST /usersAndHouseholdManagement/useRecipeByRecipeId
        Add to the history of consumption of meals at household.
        household_id: Id of the household.
        meal : [
              "Breakfast",
              "Lunch",
              "Dinner",
              "Snakes"
            ] need to be on of them
         dishes_num : flout
         recipe_id : id of recipe to use : string
         
         body : 
               user_email: list of email of the user to add.
         
      Example:
         http://127.0.0.1:8000/usersAndHouseholdManagement/useRecipeByRecipeId?household_id=2f249d7a-bca5-4ae1-87e3-cf3cba2b02b3&meal=Lunch&dishes_num=1&recipe_id=634435
         with this body
            [
               "example@example.example"
            ]
         return Null if sucseessful 

    GET /usersAndHouseholdManagement/getMealTypes
        Return list of meals types

    GET /usersAndHouseholdManagement/getAllRecipesThatHouseholdCanMake
        Return list of recipes that household can make or 404 if there no recipes
        user_mail: Email of the user to add.
        household_id: Id of the household.
         co2_weight : Default value : 0.5 : fout /// for the sorting by 2 parameters
         expiration_weight : Default value : 0.5 : fout /// for the sorting by 2 parameters

    GET /usersAndHouseholdManagement/checkIfHouseholdExistInSystem
         Return true if the hosehold exist in the system
         household_id: Id of the household.
    
    GET /usersAndHouseholdManagement/checkIfHouseholdCanMakeRecipe
         This endpoint allows users to check if a specific household has enough ingredients to make a given recipe for a specified number of dishes.
         household_id : The ID of the household. : string
         recipe_id : The ID of the recipe. : string
         dishes_num : The number of dishes to be made. Defaults to 1 if not provided. : optional[int], default=1)
         
         Returns a boolean indicating whether the household can make the specified recipe

getGasPollutionOfHouseholdInRangeDates

      Post /usersAndHouseholdManagement/getGasPollutionOfHouseholdInRangeDates
      This endpoint returns the total gas emissions of the household on the specified dates
      user_mail: Email of user in household.
      household_id: Id of the household.
      require body :
      {
        "startDate": {
          "year": 0,
          "month": 0,
          "day": 0
        },
        "endDate": {
          "year": 0,
          "month": 0,
          "day": 0
        }
      }
      example : 
      'http://127.0.0.1:8000/usersAndHouseholdManagement/getGasPollutionOfHouseholdInRangeDates?user_email=nissanyam1%40gmail.com&household_id=67fc717d-67b4-43e0-a8dc-cb5189a9c383'
      {
        "startDate": {
          "year": 2024,
          "month": 6,
          "day": 1
        },
        "endDate": {
          "year": 2024,
          "month": 7,
          "day": 10
        }
         return :
         {
           "CO2": 33428.79239999999
         }

getGasPollutionOfUserInRangeDates

      Post /usersAndHouseholdManagement/getGasPollutionOfUserInRangeDates
      This endpoint returns the total gas emissions of the user on the specified dates
      user_mail: Email of the user.

Object Definitions

RecipeBoundary

Represents a recipe object returned by the API.

    recipe_id: Unique identifier for the recipe. : int
    recipe_name: Name of the recipe. : string
    ingredients: List of ingredients in the recipe, each represented by an IngredientBoundary object. : [IngredientBoundary]
    image_url: URL of the image associated with the recipe. : string
    sumGasPollution : Dict of gas that would emmitin if the ingredients throws

recipe_instructionsBoundary

Represents a instructions of recipe object returned by the API.

       name: Name of the recipe. : string
       steps : list of steps objects : [Step]

      stepObject
       equipment: List of equipments needed to prepare the recipe : [equipment name : equipment image url] (string:string)
       ingredients: List of ingredients needed to prepare the recipe  : [ingredient name : ingredient image url] (string:string)
       length : Time to prepare the recipe : flout
       number : Step number : Int
       description : Description of what to do in this step : String
    
IngredientBoundary

Represents an ingredient object returned by the API.

    ingredient_id: Unique identifier for the ingredient. : string
    name: Name of the ingredient. : string
    amonth: Amonth of the ingredient. : flout
    unit: Unit of measurement for the amonth. : string 
    purchase_date: Date the ingredient was purchased. : string

HouseholdBoundary

Represents a household object returned by the API.

    household_id: Unique identifier for the household. : String
    household_name: Name of the household. : String
    household_image: Image associated with the household. : String
    participants: List of participants email in the household. [String] 
    ingredients: Dictionary of ingredients in the household, where keys are ingredient id and values are lists of IngredientBoundary objects. {string : [IngredientBoundary]}
    meals: List of meals in the household, where keys are meal dates and values are meal types ("Breakfast", "Lunch", "Dinner", "Snacks"), the type is a dictionary of recipe ID and value is MealBoundary. {string : {string : { string : [MealBoundary]}}}
    sumGasPollution : Dict of gas emissions that the household saved

MealBoundary

    users: list of users that take a part of this meal. ([String])
    number_of_dishes : The number of dishes that will be made from the recipe in this meal.(Double)
    sumGasPollution : Dict of gas emissions that the meal saved

UserBoundary

Represents a user object returned by the API.

    first_name: First name of the user. : string
    last_name: Last name of the user. : string
    user_email: Email of the user. : string in email format
    image: Image associated with the user.  : string
    households_ids: List of household IDs the user belongs to. [string]
    meals: date -> meal type -> recipe id -> meal. {string : {string : {string : MealBoundary}}}
    country: Country of the user. : string
    state: State of the user. : string
    sumGasPollution : Dict of gas emissions that the user saved


