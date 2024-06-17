from bson import ObjectId

from config.db import collection_pollution


class IngredientsCRUD:
    def __init__(self):
        self.collection = collection_pollution

    def search_ingredient(self, ingredient_name) -> dict:
        return self.collection.find_one({
            'ingredient': ingredient_name
        }, {'_id': 0})

    def delete_all_ingredients(self):
        result = self.collection.delete_many({})
        return result.deleted_count  # returns the number of documents deleted

    def autocomplete_ingredient(self, partial_name) -> list:
        regex_pattern = f'^{partial_name}'  # Matches any name that starts with 'partial_name'
        cursor = self.collection.find(
            {'ingredient': {'$regex': regex_pattern, '$options': 'i'}},
            {'_id': 0, 'ingredient': 1, 'ingredientId': 1, 'expirationData': 1, 'gCO2e_per_100g': 1}
        )
        return list(cursor)

    def get_all_ingredients(self) -> list:
        cursor = self.collection.find({}, {'_id': 0})
        return list(cursor)

    def delete_ingredient_by_name(self, ingredient_name):
        result = self.collection.delete_one({'name': ingredient_name})
        return result.deleted_count  # returns 1 if an ingredient was deleted, otherwise 0

    def get_ingredient_by_id(self, ingredient_id):
        return self.collection.find_one({
            'ingredientId': ingredient_id
        }, {'_id': 0})