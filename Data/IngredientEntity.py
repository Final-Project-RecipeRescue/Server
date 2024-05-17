import datetime





class IngredientEntity:
    def __init__(self, ingredient_id: str, name: str, amount: float, unit: str, purchase_date: str):
        self.id = ingredient_id
        self.name = name
        self.amount = amount
        self.unit = unit
        self.purchase_date = purchase_date

class IngredientEntitySpoonacular(IngredientEntity):
    def __init__(self, ingredient_data):
        super().__init__(str(ingredient_data.get('id')), ingredient_data.get('name'), ingredient_data.get('amount'), ingredient_data.get('unit'), "")
        self.aisle = ingredient_data.get('aisle')
        self.image = ingredient_data.get('image')
        self.meta = ingredient_data.get('meta')
        self.original = ingredient_data.get('original')
        self.original_name = ingredient_data.get('originalName')
        self.unit_long = ingredient_data.get('unitLong')
        self.unit_short = ingredient_data.get('unitShort')
        self.consistency = ingredient_data.get('consistency')
        self.measures = ingredient_data.get('measures')