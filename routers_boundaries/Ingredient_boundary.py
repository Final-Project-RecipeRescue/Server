import datetime


class ingredient_boundary:
    def __init__(self, ingredient_id: int, name: str, amount: float, unit: str, purchase_date: datetime.date):
        self.ingredient_id = ingredient_id
        self.name = name
        self.amount = amount
        self.unit = unit
        self.purchase_date = purchase_date if purchase_date is not None else None
