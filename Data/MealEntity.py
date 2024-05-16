class MealEntity:
    def __init__(self, data):
        self.type = data.get('type') if data.get('type') is not None else None
        self.users = [user for user in data.get('users', [])] if data.get('users') is not None else []
        self.recipe_id = data.get('recipe_id') if data.get('recipe_id') is not None else None
        self.number_of_dishes = data.get('number_of_dishes') if data.get('number_of_dishes') is not None else None
        self.used_date = data.get('used_date') if data.get('used_date') is not None else None


class MealEntityWithIngredients(MealEntity):
    def __init__(self, data):
        super().__init__(data)
        ingredients = data.get('ingredients', [])
        self.ingredients = [{ingredient.name: ingredient.amount}
                            for ingredient in ingredients] \
            if ingredients is not None else []
