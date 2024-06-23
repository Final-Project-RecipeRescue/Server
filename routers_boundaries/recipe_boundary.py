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
