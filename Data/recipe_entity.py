from Data.IngredientEntity import IngredientEntitySpoonacular as Ingredient
from abc import ABC, abstractmethod


class RecipeEntity(ABC):
    def __init__(self, data):
        self.id = data.get('id')
        self.image = data.get('image')
        self.imageType = data['imageType']
        self.title = data['title']


class RecipeEntityByIngredientSpoonacular(RecipeEntity):
    def __init__(self, data):
        super().__init__(data)
        self.likes = data.get('likes')
        self.missed_ingredient_count = data.get('missedIngredientCount')
        self.missed_ingredients = [Ingredient(ingredient_data) for ingredient_data in
                                   data.get('missedIngredients', [])]
        self.unused_ingredients = data.get('unusedIngredients')
        self.used_ingredient_count = data.get('usedIngredientCount')
        self.used_ingredients = [Ingredient(ingredient_data) for ingredient_data in
                                 data.get('usedIngredients', [])]


class RecipeEntityByIDSpoonacular(RecipeEntity):
    def __init__(self, data):
        super().__init__(data)
        self.servings = data['servings']
        self.readyInMinutes = data['readyInMinutes']
        self.license = data['license']
        self.sourceName = data['sourceName']
        self.sourceUrl = data['sourceUrl']
        self.spoonacularSourceUrl = data['spoonacularSourceUrl']
        self.healthScore = data['healthScore']
        self.spoonacularScore = data['spoonacularScore']
        self.pricePerServing = data['pricePerServing']
        self.creditsText = data['creditsText']
        self.dishTypes = data['dishTypes']
        self.extendedIngredients = [Ingredient(ingredient_data) for ingredient_data in
                                    data.get('extendedIngredients', [])]
        self.summary = data['summary']
        self.winePairing = data['winePairing']
