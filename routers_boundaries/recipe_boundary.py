from routers_boundaries.IngredientBoundary import IngredientBoundary


class RecipeBoundary:

    def __init__(self, recipe_id: int, recipe_name: str, ingredients: [IngredientBoundary], image_url: str
                 , sumGasPollution: int):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.image_url = image_url
        self.sumGasPollution = sumGasPollution
