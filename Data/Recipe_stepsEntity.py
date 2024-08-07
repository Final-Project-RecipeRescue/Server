class Temperature:
    def __init__(self, data):
        self.number = data.get("number") if data.get("number") is not None else None
        self.unit = data.get("unit") if data.get("unit") is not None else None

class Equipment:
    def __init__(self, data):
        self.name = data.get("name") if data.get("name") is not None else None
        self.id = data.get("id") if data.get("id") is not None else None
        self.image = data.get("image") if data.get("image") is not None else None
        self.temperature = Temperature(data.get("temperature")) if data.get("temperature") is not None else None

class Ingredient:
    def __init__(self, data):
        self.id = data.get("id") if data.get("id") is not None else None
        self.name = data.get("name") if data.get("name") is not None else None
        self.image = data.get("image") if data.get("image") is not None else None

class Length:
    def __init__(self, data):
        self.number = data.get("number") if data.get("number") is not None else None
        self.unit = data.get("unit") if data.get("unit") is not None else None

class Step:
    def __init__(self, data):
        if data.get("equipment") is not None:
            self.equipments = [Equipment(equipment) for equipment in data.get("equipment")]
        else:
            self.equipments = []
        if data.get("ingredients") is not None:
            self.ingredients = [Ingredient(ingredient) for ingredient in data.get("ingredients")]
        else:
            self.ingredients = []
        self.length = Length(data.get("length")) if data.get("length") is not None else None
        self.number = data.get("number") if data.get("number") is not None else None
        self.step = data.get("step") if data.get("step") is not None else None

class Recipe_stepsEntity:
    def __init__(self, data):
        self.name = data.get("name") if data.get("name") is not None else None
        self.steps = [Step(step) for step in data.get("steps")]
