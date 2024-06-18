class IngredientDataBoundary():
    def __init__(self, ingredient_id: str
                 , name: str
                 , expirationData: int
                 , gCO2e_per_100g: int):
        self.ingredient_id = ingredient_id
        self.name = name
        self.expirationData = expirationData
        self.gCO2e_per_100g = gCO2e_per_100g
