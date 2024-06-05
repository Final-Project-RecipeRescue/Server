import datetime


class IngredientEntity:
    def __init__(self, data):
        self.id = str(data.get("id")) if data.get("id") else None
        self.name = data.get("name") if data.get("name") else None
        self.amount = data.get("amount") if data.get("amount") else None
        self.unit = data.get("unit") if data.get("unit") else "gram"
        self.purchase_date = data.get("purchase_date") if data.get("purchase_date") else None


class IngredientEntitySpoonacular(IngredientEntity):
    def __init__(self, ingredient_data):
        super().__init__(data=ingredient_data)
        self.aisle = ingredient_data.get('aisle')
        self.image = ingredient_data.get('image')
        self.meta = ingredient_data.get('meta')
        self.original = ingredient_data.get('original')
        self.original_name = ingredient_data.get('originalName')
        self.unit_long = ingredient_data.get('unitLong')
        self.unit_short = ingredient_data.get('unitShort')
        self.consistency = ingredient_data.get('consistency')
        self.measures = ingredient_data.get('measures')
