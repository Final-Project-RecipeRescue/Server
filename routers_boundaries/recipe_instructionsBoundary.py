from typing import List
class Step:
    def __init__(self, number: int, step: str, length: int, ingredients: [str], equipments: [str]):
        self.equipment = equipments
        self.ingredients = ingredients
        self.length = length
        self.number = number
        self.description = step


class recipe_instructionsBoundary:
    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps
