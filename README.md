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

getRecipesByIngredients

    GET /recipes/getRecipesByIngredients
        Retrieves list of RecipeBoundary based on provided ingredients.
        The recipes provided may contain ingredients that are not on the ingredients list.
        ingredients: Comma-separated list of ingredients.

    Example:
        http://127.0.0.1:8000/recipes/getRecipesByIngredients?ingredients=Banana%2C%20avocado%2C%20mango%2C%20apple%2C%20salt
        
        [
          {
            "recipe_id": 634048,
            "recipe_name": "Banana Chocolate Pudding",
            "ingredients": [
              {
                "ingredient_id": "9040",
                "name": "bananas",
                "amount": 472,
                "unit": "gram",
                "purchase_date": null
              },
              {
                "ingredient_id": "19165",
                "name": "cocoa powder",
                "amount": 28.67,
                "unit": "gram",
                "purchase_date": null
              },
              {
                "ingredient_id": "16098",
                "name": "peanut butter",
                "amount": 129,
                "unit": "gram",
                "purchase_date": null
              },
              {
                "ingredient_id": "9037",
                "name": "avocado",
                "amount": 201,
                "unit": "gram",
                "purchase_date": null
              }
            ],
            "image_url": "https://img.spoonacular.com/recipes/634048-312x231.jpg"
          },...
        ]

getRecipesByIngredientsWithoutMissedIngredients

    GET /recipes/getRecipesByIngredientsWithoutMissedIngredients
        Retrieves list of RecipeBoundary based on provided ingredients, excluding those with missed ingredients.
        ingredients: Comma-separated list of ingredients.

getRecipeByID

    GET /recipes/getRecipeByID/{recipe_id}
        Retrieves a RecipeBoundary by its ID.
        recipe_id: ID of the recipe.

getRecipesByName

    GET /recipes/getRecipesByName/{recipe_name}
        Returns a list of recipes in this form:
        {
            "recipe_id": int,
            "recipe_name": string,
            "ingredients": [],
            "image_url": string
        }
        recipe_name: Name of the recipe.

    Example
        http://127.0.0.1:8000/recipes/getRecipesByName/Banana%20Chocolate%20Pudding
        
        [
          {
            "recipe_id": 634048,
            "recipe_name": "Banana Chocolate Pudding",
            "ingredients": [],
            "image_url": "https://img.spoonacular.com/recipes/634048-312x231.jpg"
          },
          {
            "recipe_id": 634047,
            "recipe_name": "Banana Chocolate Pudding Cake",
            "ingredients": [],
            "image_url": "https://img.spoonacular.com/recipes/634047-312x231.jpg"
          }
        ]

getRecipeInstructions

    GET /getRecipeInstructions/{recipe_id}
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
    
    DELETE /delete_household
        Delete household by householdID
        household_id : Id of household

    POST /add_user
        Create new user in system
        user : UserInputForAddUser
        user_mail: Email of the user.

    GET /get_user
        Return UserBoundary by user mail
    
    DELETE /delete_user
        Remove user from system and remove him from households
        user_mail: Email of the user creating the household.

    GET /get_household_user_by_id
        Retuen a HouseholdBoundary by user mail and household id.
        user_mail: Email of the user.
        household_id : Id of household

    GET /get_household_user_by_name
        Return a list of HouseholdBoundary with this household_name.
        user_mail: Email of the user.
        household_name : Name of household

    GET /get_all_household_details_by_user_mail
        Detailed information about the user's households, including a list of each household's available ingredients. 
        Return a list of HouseholdBoundary or Null if there is a problem with the user's email 
        user_mail: Email of the user.

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

    GET /get_all_recipes_that_household_can_make
        Return list of recipes that household can make or 404 if there no recipes
        user_mail: Email of the user to add.
        household_id: Id of the household.
        
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
