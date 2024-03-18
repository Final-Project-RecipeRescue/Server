import os
from typing import List

import requests
from dotenv import load_dotenv
load_dotenv()

class SpoonacularAPI:
    _instance = None
    api_key = None

    @staticmethod
    def get_instance():
        if SpoonacularAPI._instance is None:
            SpoonacularAPI._instance = SpoonacularAPI()
        return SpoonacularAPI._instance
    def __init__(self):
        if SpoonacularAPI._instance is not None:
            raise Exception("Singleton instance already exists.")
        self.base_url = "https://api.spoonacular.com"
        self.initialized = True
        self.api_key=os.getenv("SPOONACULAR_API_KEY")
        SpoonacularAPI._instance = self


    async def find_recipes_by_ingredients(self, ingredients:List[str], number=10, ranking=2,ignorePantry=True):
        url = f"{self.base_url}/recipes/findByIngredients"
        headers = {
            "x-api-key": self.api_key
        }
        params = {
            "ingredients": ",".join(ingredients),
            "number": number,
            "ranking":ranking,
            "ignorePantry":ignorePantry
        }
        response = requests.get(url,headers=headers, params=params)
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print("Error:", response.status_code)
            return None