class IngredientDataBoundary:
    def __init__(self, ingredient_id: str
                 , name: str
                 , days_to_expire: int
                 , gCO2e_per_100g: int):
        self.ingredient_id = ingredient_id
        self.name = name
        self.days_to_expire = days_to_expire
        self.gCO2e_per_100g = gCO2e_per_100g
