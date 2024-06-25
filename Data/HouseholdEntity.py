from typing import List


class HouseholdEntity:
    def __init__(self, data):
        self.id = data.get('id') if data.get('id') else ""
        self.name = data.get('name') if data.get('name') else None
        self.image = data.get('image') if data.get('image') else None
        self.participants = data.get('participants') if data.get('participants') else []
        self.ingredients = data.get('ingredients') if data.get('ingredients') else {}
        self.meals = data.get('meals') if data.get('meals') else {}


class HouseholdEntityWithGas(HouseholdEntity):
    def __init__(self, data):
        super().__init__(data)
        self.sum_gas_pollution = data.get('sum_gas_pollution', {str, float}) if data.get('sum_gas_pollution') else None
