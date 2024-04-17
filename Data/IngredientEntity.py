import datetime


class IngredientEntitySpoonacular:
    def __init__(self, ingredient_data):
        self.aisle = ingredient_data.get('aisle')
        self.amount = ingredient_data.get('amount')
        self.id = ingredient_data.get('id')
        self.image = ingredient_data.get('image')
        self.meta = ingredient_data.get('meta')
        self.name = ingredient_data.get('name')
        self.original = ingredient_data.get('original')
        self.original_name = ingredient_data.get('originalName')
        self.unit = ingredient_data.get('unit')
        self.unit_long = ingredient_data.get('unitLong')
        self.unit_short = ingredient_data.get('unitShort')
        self.consistency = ingredient_data.get('consistency')
        self.measures = ingredient_data.get('measures')


class IngredientEntity:
    def __init__(self, id: int, name: str, amount: float, unit: str, purchase_date: str):
        self.id = id
        self.name = name
        self.amount = amount
        self.unit = unit
        self.purchase_date = purchase_date