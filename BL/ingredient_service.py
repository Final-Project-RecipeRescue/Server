from typing import List, Optional

from DAL.IngredientsCRUD import IngredientsCRUD
from routers_boundaries.IngredientDataBoundary import IngredientDataBoundary

ingredientsCRUD = IngredientsCRUD()


def to_ingredient_data_boundary(ingredient) -> IngredientDataBoundary:
    ingredient_id = ingredient['ingredientId']
    name = ingredient['ingredient']
    expirationData = ingredient['expirationData']
    gCO2e_per_100g = ingredient['gCO2e_per_100g']
    return IngredientDataBoundary(ingredient_id, name, expirationData, gCO2e_per_100g)


class IngredientService:
    def get_all_ingredients(self) -> [IngredientDataBoundary]:
        ingredients = []
        for ingredient in ingredientsCRUD.get_all_ingredients():
            ingredients.append(to_ingredient_data_boundary(ingredient))
        return ingredients

    def autocomplete_by_ingredient_name(self, partial_name: str) -> Optional[List[IngredientDataBoundary]]:
        ingredients = []
        for ingredient in ingredientsCRUD.autocomplete_ingredient(partial_name):
            ingredients.append(to_ingredient_data_boundary(ingredient))
        return ingredients

    def get_ingredient_by_id(self, ingredient_id: int) -> Optional[IngredientDataBoundary]:
        ingredient = ingredientsCRUD.get_ingredient_by_id(ingredient_id)
        return to_ingredient_data_boundary(ingredient)
