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

        self.ingredients = [{list(ingredient.keys())[0]: list(ingredient.values())[0]}
                            for ingredient in data.get('ingredients', [])] \
            if data.get('ingredients') is not None else []
