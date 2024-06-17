import datetime


class IngredientBoundary:

    def __init__(self, ingredient_id: str, name: str, amount: float, unit: str, purchase_date: datetime.date):
        self.ingredient_id = ingredient_id
        self.name = name
        self.amount = amount
        self.unit = unit
        if purchase_date is None:
            self.purchase_date = None
        else:
            self.purchase_date = purchase_date.strftime("%Y-%m-%d") if purchase_date else datetime.now().strftime(
                "%Y-%m-%d")


class IngredientBoundaryWithExpirationData(IngredientBoundary):
    def __init__(self, ingredient: IngredientBoundary, expiration_date: datetime.date):
        super().__init__(
            ingredient.ingredient_id,
            ingredient.name,
            ingredient.amount,
            ingredient.unit,
            ingredient.purchase_date
        )
        if expiration_date is None:
            self.expiration_date = None
        else:
            self.expiration_date = expiration_date.strftime("%Y-%m-%d")
