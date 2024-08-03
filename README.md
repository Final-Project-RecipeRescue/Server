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
## Possible Errors

- **400 Bad Request**: Returned if the `ingredients` parameter is empty or improperly formatted.
- **404 Not Found**: Returned if no recipes match the provided ingredients or if an error occurs during recipe retrieval.
- **500 Internal Server Error**: Returned if there is a server-side error while processing the request.


getRecipesByIngredientsWithoutMissingIngredients

    GET /recipes/getRecipesByIngredientsWithoutMissingIngredients
        Retrieves list of RecipeBoundary based on provided ingredients, excluding those with missing ingredients.
        ingredients: Comma-separated list of ingredients.

getRecipeByID

    GET /recipes/getRecipeByID/{recipe_id}
        Retrieves a RecipeBoundary by its ID.
        recipe_id: ID of the recipe.

getRecipesByName

    GET /recipes/getRecipesByName/{recipe_name}
        Returns a list of RecipeBoundary by its name

getRecipeInstructions

    GET /recipes/getRecipeInstructions/{recipe_id}
        Retrieves a list of recipe_instructionsBoundary by this Id
        recipe_id: ID of the recipe.
        Return list of instructions in this from:
        [
            {
                name : str
                steps : 
                    [
                        {
                            number : int
                            description : str
                            length : flout
                            ingredients : 
                                [
                                    { Ingredient Name : Ingredient image}
                                ]
                            equipment :
                                [
                                    {Equipment Name : Equipment Image
                                ]
                        }
                    ]
            }
        ]
    Example
        http://127.0.0.1:8000/recipes/getRecipeInstructions/324694
        
        [
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
                "length": null,
                "number": 1,
                "description": "Preheat the oven to 200 degrees F."
              },
              {
                "equipment": [
                  {
                    "whisk": "https://spoonacular.com/cdn/equipment_100x100/whisk.png"
                  },
                  {
                    "bowl": "https://spoonacular.com/cdn/equipment_100x100/bowl.jpg"
                  }
                ],
                "ingredients": [
                  {
                    "light brown sugar": "https://spoonacular.com/cdn/ingredients_100x100/light-brown-sugar.jpg"
                  },
                  {
                    "granulated sugar": "https://spoonacular.com/cdn/ingredients_100x100/sugar-in-bowl.png"
                  },
                  {
                    "baking powder": "https://spoonacular.com/cdn/ingredients_100x100/white-powder.jpg"
                  },
                  {
                    "baking soda": "https://spoonacular.com/cdn/ingredients_100x100/white-powder.jpg"
                  },
                  {
                    "pecans": "https://spoonacular.com/cdn/ingredients_100x100/pecans.jpg"
                  },
                  {
                    "all purpose flour": "https://spoonacular.com/cdn/ingredients_100x100/flour.png"
                  },
                  {
                    "salt": "https://spoonacular.com/cdn/ingredients_100x100/salt.jpg"
                  }
                ],
                "length": null,
                "number": 2,
                "description": "Whisk together the flour, pecans, granulated sugar, light brown sugar, baking powder, baking soda, and salt in a medium bowl."
              },
              {
                "equipment": [
                  {
                    "whisk": "https://spoonacular.com/cdn/equipment_100x100/whisk.png"
                  },
                  {
                    "bowl": "https://spoonacular.com/cdn/equipment_100x100/bowl.jpg"
                  }
                ],
                "ingredients": [
                  {
                    "vanilla extract": "https://spoonacular.com/cdn/ingredients_100x100/vanilla-extract.jpg"
                  },
                  {
                    "vanilla bean": "https://spoonacular.com/cdn/ingredients_100x100/vanilla.jpg"
                  },
                  {
                    "buttermilk": "https://spoonacular.com/cdn/ingredients_100x100/buttermilk.jpg"
                  },
                  {
                    "butter": "https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"
                  },
                  {
                    "egg": "https://spoonacular.com/cdn/ingredients_100x100/egg.png"
                  }
                ],
                "length": null,
                "number": 3,
                "description": "Whisk together the eggs, buttermilk, butter and vanilla extract and vanilla bean in a small bowl."
              },
              {
                "equipment": [],
                "ingredients": [
                  {
                    "egg": "https://spoonacular.com/cdn/ingredients_100x100/egg.png"
                  }
                ],
                "length": null,
                "number": 4,
                "description": "Add the egg mixture to the dry mixture and gently mix to combine. Do not overmix."
              },
              {
                "equipment": [],
                "ingredients": [],
                "length": {
                  "number": 15,
                  "unit": "minutes"
                },
                "number": 5,
                "description": "Let the batter sit at room temperature for at least 15 minutes and up to 30 minutes before using."
              },
              {
                "equipment": [
                  {
                    "frying pan": "https://spoonacular.com/cdn/equipment_100x100/pan.png"
                  }
                ],
                "ingredients": [
                  {
                    "butter": "https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"
                  }
                ],
                "length": {
                  "number": 3,
                  "unit": "minutes"
                },
                "number": 6,
                "description": "Heat a cast iron or nonstick griddle pan over medium heat and brush with melted butter. Once the butter begins to sizzle, use 2 tablespoons of the batter for each pancake and cook until the bubbles appear on the surface and the bottom is golden brown, about 2 minutes, flip over and cook until the bottom is golden brown, 1 to 2 minutes longer."
              },
              {
                "equipment": [
                  {
                    "oven": "https://spoonacular.com/cdn/equipment_100x100/oven.jpg"
                  }
                ],
                "ingredients": [],
                "length": null,
                "number": 7,
                "description": "Transfer the pancakes to a platter and keep warm in a 200 degree F oven."
              },
              {
                "equipment": [],
                "ingredients": [
                  {
                    "bourbon": "https://spoonacular.com/cdn/ingredients_100x100/bourbon.png"
                  },
                  {
                    "butter": "https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"
                  }
                ],
                "length": null,
                "number": 8,
                "description": "Serve 6 pancakes per person, top each with some of the bourbon butter."
              },
              {
                "equipment": [],
                "ingredients": [
                  {
                    "powdered sugar": "https://spoonacular.com/cdn/ingredients_100x100/powdered-sugar.jpg"
                  },
                  {
                    "maple syrup": "https://spoonacular.com/cdn/ingredients_100x100/maple-syrup.png"
                  }
                ],
                "length": null,
                "number": 9,
                "description": "Drizzle with warm maple syrup and dust with confectioners' sugar."
              },
              {
                "equipment": [],
                "ingredients": [
                  {
                    "fresh mint": "https://spoonacular.com/cdn/ingredients_100x100/mint.jpg"
                  },
                  {
                    "pecans": "https://spoonacular.com/cdn/ingredients_100x100/pecans.jpg"
                  }
                ],
                "length": null,
                "number": 10,
                "description": "Garnish with fresh mint sprigs and more toasted pecans, if desired."
              }
            ]
          },
          {
            "name": "Bourbon Molasses Butter",
            "steps": [
              {
                "equipment": [
                  {
                    "sauce pan": "https://spoonacular.com/cdn/equipment_100x100/sauce-pan.jpg"
                  }
                ],
                "ingredients": [
                  {
                    "bourbon": "https://spoonacular.com/cdn/ingredients_100x100/bourbon.png"
                  },
                  {
                    "sugar": "https://spoonacular.com/cdn/ingredients_100x100/sugar-in-bowl.png"
                  }
                ],
                "length": null,
                "number": 1,
                "description": "Combine the bourbon and sugar in a small saucepan and cook over high heat until reduced to 3 tablespoons, remove and let cool."
              },
              {
                "equipment": [
                  {
                    "food processor": "https://spoonacular.com/cdn/equipment_100x100/food-processor.png"
                  }
                ],
                "ingredients": [
                  {
                    "molasses": "https://spoonacular.com/cdn/ingredients_100x100/molasses.jpg"
                  },
                  {
                    "bourbon": "https://spoonacular.com/cdn/ingredients_100x100/bourbon.png"
                  },
                  {
                    "butter": "https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"
                  },
                  {
                    "salt": "https://spoonacular.com/cdn/ingredients_100x100/salt.jpg"
                  }
                ],
                "length": null,
                "number": 2,
                "description": "Put the butter, molasses, salt and cooled bourbon mixture in a food processor and process until smooth."
              },
              {
                "equipment": [
                  {
                    "plastic wrap": "https://spoonacular.com/cdn/equipment_100x100/plastic-wrap.jpg"
                  },
                  {
                    "bowl": "https://spoonacular.com/cdn/equipment_100x100/bowl.jpg"
                  }
                ],
                "ingredients": [
                  {
                    "wrap": "https://spoonacular.com/cdn/ingredients_100x100/flour-tortilla.jpg"
                  }
                ],
                "length": {
                  "number": 60,
                  "unit": "minutes"
                },
                "number": 3,
                "description": "Scrape into a bowl, cover with plastic wrap and refrigerate for at least 1 hour to allow the flavors to meld."
              },
              {
                "equipment": [],
                "ingredients": [],
                "length": {
                  "number": 30,
                  "unit": "minutes"
                },
                "number": 4,
                "description": "Remove from the refrigerator about 30 minutes before using to soften."
              }
            ]
          }
        ]

Ingredients

getAllSystemIngredients

    GET /ingredients/getAllSystemIngredients
     Retrieves a list of ingredients in this from:
      {
         "ingredient_id": String,
         "name": Name of the ingredient,
         "expirationData": number of days to expire : Int
         "gCO2e_per_100g": The amonth of carbon dioxide emitted if it is thrown : Int
      }
    
autocompleteIngredient

       GET /ingredients/autocompleteIngredient
       Retrieves a list of ingredients whose prefix is partial_name
       partial_name : String

getIngredientById

      GET /ingredients/getIngredientById
      Retrieves a ingredient by id
      ingredient_id: int

getIngredientByName

      Retrieves a ingredient by name
      ingredient_name: str

Users and Household Operations

createNewHousehold

    POST /usersAndHouseholdManagement/usersAndHouseholdManagement/createNewHousehold
        Creates a new household.
        user_mail: Email of the user creating the household.
        household_name: Name of the household.
        
    Example
    http://127.0.0.1:8000/usersAndHouseholdManagement/createNewHousehold?user_mail=example%40example.example&household_name=example
    with body
        {
          "ingredients": [
            {
              "ingredient_id": null,
              "name": "Avocado",
              "amonth": 15,
              "unit": null
            }
          ]
        }
    **The list of components is optional, meaning you don't have to do it
    Return value
    {
      "message": "Household added successfully",
      "household_id": "e69f3780-7eaa-4602-8b86-1fd6b38ccd64"
    }
        
deleteHousehold

    DELETE /usersAndHouseholdManagement/deleteHousehold
        Delete household by householdID
        household_id : Id of household

addUser

    POST /usersAndHouseholdManagement/addUser
        Create new user in system
        user : UserInputForAddUser
        user_mail: Email of the user.
    
    Example
    http://127.0.0.1:8000/usersAndHouseholdManagement/addUser
        with this body 
        {
          "first_name": "example",
          "last_name": "example",
          "email": "example@example.example",
          "country": "example",
          "state": "example"
        }
    Return value
        {
          "message": "Successfully Added User"
        }

getUser

    GET /usersAndHouseholdManagement/getUser
        Return UserBoundary by user mail
    
    Example
    http://127.0.0.1:8000/usersAndHouseholdManagement/getUser?user_email=example%40example.example
    
    Return value:
      {
        "first_name": "Nissan",
        "last_name": "Yamin",
        "user_email": "nissanyam1@gmail.com",
        "image": null,
        "households": [
          "67fc717d-67b4-43e0-a8dc-cb5189a9c383",
          "bd616751-cc28-41b5-9719-fbf1b1f52df3"
        ],
        "meals": {
          "2024-06-26": {
            "Lunch": {
              "635058": {
                "users": [
                  "nissanyam1@gmail.com"
                ],
                "number_of_dishes": 0,
                "sum_gas_pollution": {
                  "CO2": 0
                }
              },
              "643514": {
                "users": [
                  "nissanyam1@gmail.com"
                ],
                "number_of_dishes": 0,
                "sum_gas_pollution": {
                  "CO2": 0
                }
              },
              "664932": {
                "users": [
                  "nissanyam1@gmail.com"
                ],
                "number_of_dishes": 0,
                "sum_gas_pollution": {
                  "CO2": 0
                }
              }
            }
          },
          "2024-06-27": {
            "Lunch": {
              "643514": {
                "users": [
                  "nissanyam1@gmail.com"
                ],
                "number_of_dishes": 0,
                "sum_gas_pollution": {
                  "CO2": 0
                }
              }
            }
          }
        },
        "country": "Israel",
        "state": "Haifa District",
        "sum_gas_pollution": {
          "CO2": 0
        }
      }

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


