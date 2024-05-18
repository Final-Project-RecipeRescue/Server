class MealEntity:
    def __init__(self, data):
        self.users = [user for user in data.get('users', [])] if data.get('users') is not None else []
        self.number_of_dishes = data.get('number_of_dishes') if data.get('number_of_dishes') is not None else None

