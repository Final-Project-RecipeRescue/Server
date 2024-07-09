import datetime


class IngredientBoundary:

    def __init__(self, ingredient_id: str, name: str, amount: float, unit: str, purchase_date: datetime.date or str):
        self.ingredient_id = ingredient_id
        self.name = name
        self.amount = amount
        self.unit = unit
        if purchase_date is None:
            self.purchase_date = None
        else:
            if isinstance(purchase_date, datetime.date):
                self.purchase_date = purchase_date.strftime("%Y-%m-%d")
            elif isinstance(purchase_date, str):
                try:
                    datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
                    self.purchase_date = purchase_date
                except ValueError:
                    pass


class IngredientBoundaryWithExpirationData(IngredientBoundary):
    def __init__(self, ingredient: IngredientBoundary, expiration_date: datetime.date or str):
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
            if isinstance(expiration_date, datetime.date):
                self.expiration_date = expiration_date.strftime("%Y-%m-%d")
            elif isinstance(expiration_date, str):
                try:
                    datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
                    self.expiration_date = expiration_date
                except ValueError:
                    pass
