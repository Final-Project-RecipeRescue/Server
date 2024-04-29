from bson import ObjectId

from config.db import collection_ingredients


class IngredientsCRUD:
    def __init__(self):
        self.collection = collection_ingredients

    def search_ingredient(self, ingredient_name) -> dict:
        return self.collection.find_one({
            'name': ingredient_name
        }, {'_id': 0})

    def delete_all_ingredients(self):
        result = self.collection.delete_many({})
        return result.deleted_count  # returns the number of documents deleted

    def autocomplete_ingredient(self, partial_name) -> list:
        regex_pattern = f'^{partial_name}'  # Matches any name that starts with 'partial_name'
        cursor = self.collection.find(
            {'name': {'$regex': regex_pattern, '$options': 'i'}},
            {'_id': 0, 'name': 1, 'id': 1}  # Projection including both id and name
        )
        return list(cursor)

    def get_all_ingredients(self) -> list:
        cursor = self.collection.find({}, {'_id': 0})
        return list(cursor)

    def delete_ingredient_by_name(self, ingredient_name):
        result = self.collection.delete_one({'name': ingredient_name})
        return result.deleted_count  # returns 1 if an ingredient was deleted, otherwise 0


