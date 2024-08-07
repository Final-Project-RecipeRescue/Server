from Data.IngredientEntity import IngredientEntitySpoonacular as Ingredient
from abc import ABC


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
        self.missing_ingredients_count = data.get('missedIngredientCount')
        self.missing_ingredients = [Ingredient(ingredient_data) for ingredient_data in
                                    data.get('missedIngredients', [])]
        self.unused_ingredients = data.get('unusedIngredients')
        self.used_ingredient_count = data.get('usedIngredientCount')
        self.used_ingredients = [Ingredient(ingredient_data) for ingredient_data in
                                 data.get('usedIngredients', [])]


class RecipeEntityByIDSpoonacular(RecipeEntity):
    def __init__(self, data):
        super().__init__(data)
        # self.servings = data['servings'] if data['servings'] is not None else None
        # self.readyInMinutes = data['readyInMinutes'] if data['readyInMinutes'] is not None else None
        # self.license = data['license'] if data['license'] is not None else None
        # self.sourceName = data['sourceName'] if data['sourceName'] is not None else None
        # self.sourceUrl = data['sourceUrl'] if data['sourceUrl'] is not None else None
        # self.spoonacularSourceUrl = data['spoonacularSourceUrl'] if data['spoonacularSourceUrl'] is not None else None
        # self.healthScore = data['healthScore'] if data['healthScore'] is not None else None
        # self.spoonacularScore = data['spoonacularScore'] if data['spoonacularScore'] is not None else None
        # self.pricePerServing = data['pricePerServing'] if data['pricePerServing'] is not None else None
        # self.creditsText = data['creditsText'] if data['creditsText'] is not None else None
        # self.dishTypes = data['dishTypes'] if data['dishTypes'] is not None else None
        self.extendedIngredients = [Ingredient(ingredient_data) for ingredient_data in
                                    data.get('extendedIngredients', [])]
        self.summary = data['summary'] if data['summary'] is not None else None
        # self.winePairing = data['winePairing'] if data['winePairing'] is not None else None
