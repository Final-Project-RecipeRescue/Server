from typing import List
from routers_boundaries.Ingredient_boundary import ingredient_boundary

class RecipeBoundary:
    def __init__(self,
                 id: int,
                 recipe_name: str,
                 ingredients: [ingredient_boundary],
                 image_url: str
                 ):
        self.id = id
        self.recipe_name = recipe_name
        self.ingredients = ingredients
        self.image_url = image_url
        pass
