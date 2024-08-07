from typing import List, Dict


class Step:
    def __init__(self, number: int, step: str, length: float, ingredients: List[Dict[str, str]],
                 equipments: List[Dict[str, str]]):
        self.equipment = equipments
        self.ingredients = ingredients
        self.length = length
        self.number = number
        self.description = step


class RecipeInstructionsBoundary:
    def __init__(self, name: str, steps: List[Step]):
        self.name = name
        self.steps = steps
        self.total_length = self.calculate_total_length()

    def calculate_total_length(self) -> float:
        total_length = 0
        for step in self.steps:
            if step.length:
                total_length += step.length
        return total_length
