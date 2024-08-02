from bson import ObjectId

from config.db import collection_pollution
from config.db import collection_ingredients

import logging

logger = logging.getLogger("my_logger")


class IngredientsCRUD:
    def __init__(self):
        self.collection = collection_pollution
        logger.info("IngredientsCRUD initialized with collection_pollution")

    def search_ingredient(self, ingredient_name) -> dict:
        try:
            ingredient = self.collection.find_one({
                'ingredient': ingredient_name
            }, {'_id': 0})
            logger.info(f"Ingredient '{ingredient_name}' searched successfully.")
            return ingredient
        except Exception as e:
            logger.error(f"Error searching for ingredient '{ingredient_name}': {e}")
            raise

    def delete_all_ingredients(self):
        try:
            result = self.collection.delete_many({})
            logger.info(f"All ingredients deleted. Count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting all ingredients: {e}")
            raise

    def autocomplete_ingredient(self, partial_name) -> list:
        try:
            regex_pattern = f'^{partial_name}'  # Matches any name that starts with 'partial_name'
            cursor = self.collection.find(
                {'ingredient': {'$regex': regex_pattern, '$options': 'i'}},
                {'_id': 0, 'ingredient': 1, 'ingredientId': 1, 'expirationData': 1, 'gCO2e_per_100g': 1}
            )
            results = list(cursor)
            logger.info(f"Autocomplete search for '{partial_name}' returned {len(results)} results.")
            return results
        except Exception as e:
            logger.error(f"Error during autocomplete search for '{partial_name}': {e}")
            raise
    def get_all_ingredients(self) -> list:
        try:
            cursor = self.collection.find({}, {'_id': 0})
            results = list(cursor)
            logger.info(f"Retrieved all ingredients. Count: {len(results)}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving all ingredients: {e}")
            raise

    def delete_ingredient_by_name(self, ingredient_name):
        try:
            result = self.collection.delete_one({'ingredient': ingredient_name})
            logger.info(f"Ingredient '{ingredient_name}' deletion count: {result.deleted_count}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting ingredient '{ingredient_name}': {e}")
            raise

    def get_ingredient_by_id(self, ingredient_id):
        try:
            ingredient = self.collection.find_one({
                'ingredientId': ingredient_id
            }, {'_id': 0})
            logger.info(f"Ingredient with ID '{ingredient_id}' retrieved successfully.")
            return ingredient
        except Exception as e:
            logger.error(f"Error retrieving ingredient with ID '{ingredient_id}': {e}")
            raise