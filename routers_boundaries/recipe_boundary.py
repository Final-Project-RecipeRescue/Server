from typing import List, Dict

from routers_boundaries.IngredientBoundary import IngredientBoundary


class RecipeBoundary:

    def __init__(self, recipe_id: int, recipe_name: str, ingredients: List[IngredientBoundary], image_url: str):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.image_url = image_url


class RecipeBoundaryWithGasPollution(RecipeBoundary):
    def __init__(self, recipe_id: int, recipe_name: str, ingredients: [IngredientBoundary], image_url: str,
                 sumGasPollution: {str: int}):
        super().__init__(recipe_id, recipe_name, ingredients, image_url)
        self.sumGasPollution = sumGasPollution

    def __init__(self, recipe: RecipeBoundary, sumGasPollution: Dict[str, int]):
        super().__init__(recipe.recipe_id, recipe.recipe_name, recipe.ingredients, recipe.image_url)
        self.sumGasPollution = sumGasPollution

    def __lt__(self, other, co2_weight=0.5, expiration_weight=0.5):
        return self.composite_score(co2_weight, expiration_weight) < other.composite_score(co2_weight,
                                                                                           expiration_weight)

    def composite_score(self, co2_weight=0.5, expiration_weight=0.5, gas_type: str = "CO2"):
        # Normalize CO2 emissions and expiration date
        co2_score = self.sumGasPollution.get(gas_type, self.sumGasPollution.get("CO2", 0))
        expiration_date_score = 0
        try:
            expiration_date_score = self.closest_expiration_days
        except Exception:
            pass
        # Combine the scores with specified weights
        return co2_weight * co2_score - expiration_weight * expiration_date_score

    def set_closest_expiration_days(self, days_to_expire: int):
        self.closest_expiration_days = days_to_expire
