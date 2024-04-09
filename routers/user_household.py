from fastapi import APIRouter
from BL.users_household_service import UsersHouseholdService

router = APIRouter(prefix='/users_household',tags=['users and household operations'])## tag is description of router


from fastapi import APIRouter

router = APIRouter(prefix='/users_household', tags=['users and household operations'])

user_household_service = UsersHouseholdService()

# Adding a new household with the user who created it
@router.post("/add_household")
async def add_household(user_mail: str, household_name: str):
    if await user_household_service.create_household(user_mail, household_name) == 1:
        return {"message": "Household added successfully"}
    else:
        return {"message": "Household Not added successfully"}


# Adding a new user
@router.post("/add_user")
async def add_user(first_name: str, last_name: str, email: str ):
    # Logic to add a new user
    if await user_household_service.create_user(first_name, last_name, email) == 1:
        return {"message": "User added successfully"}
    else:
        return {"message": "User not added successfully"}

'''
# Adding a new user to the household and defining him as a participant and not as an owner
@router.post("/add_user_to_household")
async def add_user_to_household(household_id: int, user_id: int):
    # Logic to add a user to a household
    # Assume household_id and user_id validation
    household = households[household_id]
    household["participants"].append(user_id)
    return {"message": "User added to household as a participant"}

# Adding ingredients to the household
@router.post("/add_ingredients_to_household")
async def add_ingredients_to_household(household_id: int, ingredients: list):
    # Logic to add ingredients to a household
    # Assume household_id validation
    household = households[household_id]
    household["ingredients"].extend(ingredients)
    return {"message": "ingredients added to household"}

# Receiving the ingredients in the household
@router.get("/get_ingredients_in_household/{household_id}")
async def get_ingredients_in_household(household_id: int):
    # Logic to get ingredients in a household
    # Assume household_id validation
    household = households[household_id]
    return {"ingredients": household.get("ingredients", [])}

# Getting all the user's households
@router.get("/get_user_households/{user_id}")
async def get_user_households(user_id: int):
    # Logic to get all households of a user
    user_households = [household for household in households if user_id in household["participants"]]
    return {"user_households": user_households}

# Getting all households in the software
@router.get("/get_all_households")
async def get_all_households():
    # Logic to get all households
    return {"all_households": households}

# Acceptance of all users in the household
@router.post("/accept_all_users/{household_id}")
async def accept_all_users(household_id: int):
    # Logic to accept all users in a household
    # Assume household_id validation
    household = households[household_id]
    household["participants_accepted"] = household.get("participants", [])
    return {"message": "All users accepted in the household"}

# Setting up an additional manager for the household
@router.post("/add_manager_to_household")
async def add_manager_to_household(household_id: int, manager_id: int):
    # Logic to add a manager to a household
    # Assume household_id validation
    household = households[household_id]
    household["managers"].append(manager_id)
    return {"message": "Manager added to household"}

# Accepting all users
@router.post("/get_all_users")
async def accept_all_users():
    # Logic to accept all users
    for household in households:
        household["participants_accepted"] = household.get("participants", [])
    return {"message": "All users accepted"}

# Receiving all the recipes that the household consumed
@router.get("/get_consumed_recipes/{household_id}")
async def get_consumed_recipes(household_id: int):
    # Logic to get all consumed recipes by a household
    # Assume household_id validation
    household_recipes = [recipe for recipe in recipes_consumed if recipe["household_id"] == household_id]
    return {"consumed_recipes": household_recipes}

# Receiving all the ingredients that the household threw away in a certain period of time
@router.get("/get_thrown_away_ingredients/{household_id}")
async def get_thrown_away_ingredients(household_id: int, start_date: str, end_date: str):
    # Logic to get thrown away ingredients by a household within a certain period
    # Assume household_id validation and date parsing
    return {"thrown_away_ingredients": []}  # Placeholder for actual logic

'''