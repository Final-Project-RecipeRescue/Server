from typing import List, Optional

from DAL.IngredientsCRUD import IngredientsCRUD
from routers_boundaries.IngredientDataBoundary import IngredientDataBoundary

ingredientsCRUD = IngredientsCRUD()


def to_ingredient_data_boundary(ingredient) -> IngredientDataBoundary:
    ingredient_id = str(ingredient['ingredientId'])
    name = ingredient['ingredient']
    days_to_expire = ingredient['expirationData']
    gCO2e_per_100g = ingredient['gCO2e_per_100g']
    return IngredientDataBoundary(ingredient_id, name, days_to_expire, gCO2e_per_100g)


class IngredientService:
    def get_all_ingredients(self) -> [IngredientDataBoundary]:
        ingredients = []
        for ingredient in ingredientsCRUD.get_all_ingredients():
            ingredients.append(to_ingredient_data_boundary(ingredient))
        return ingredients

    def autocomplete_by_ingredient_name(self, partial_name: str) -> Optional[List[IngredientDataBoundary]]:
        ingredients_data = ingredientsCRUD.autocomplete_ingredient(partial_name)
        rv = []
        if ingredients_data is not None:
            for ingredient in ingredients_data:
                rv.append(to_ingredient_data_boundary(ingredient))
        return rv

    def get_ingredient_by_id(self, ingredient_id) -> Optional[IngredientDataBoundary]:
        ingredient = ingredientsCRUD.get_ingredient_by_id(int(ingredient_id))
        if ingredient is not None:
            return to_ingredient_data_boundary(ingredient)

    def search_ingredient_by_name(self, name: str) -> Optional[IngredientDataBoundary]:
        ingredient = ingredientsCRUD.search_ingredient(name.lower())
        if ingredient is not None:
            return to_ingredient_data_boundary(ingredient)
