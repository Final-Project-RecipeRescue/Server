import datetime


class ingredient_boundary:
    def __init__(self, ingredient_id: int, name: str, amount: float, unit: str, purchase_date: datetime.date):
        self.ingredient_id = ingredient_id
        self.name = name
        self.amount = amount
        self.unit = unit
        if purchase_date is None:
            self.purchase_date = None
        else:
            self.purchase_date = purchase_date.strftime("%Y-%m-%d") if purchase_date else datetime.now().strftime("%Y-%m-%d")