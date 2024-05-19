import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_pass = os.getenv("MONGO_PASS")
mongo_user = os.getenv("MONGO_USER")

uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.5yvw6hf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client.recipe_rescue_db

collection_pollution = db["pollution"]
collection_ingredients = db["ingredients"]
collection_recipes = db["recipes"]
collection_recipes_instructions = db["recipes_instructions"]
