from Data.MealEntity import MealEntityWithIngredients
from routers_boundaries.MealBoundary import MealBoundaryWithIngredients


class UserEntity:
    def __init__(self, data):
        self.first_name = data.get('first_name') if data.get('first_name') else None
        self.last_name = data.get('last_name') if data.get('last_name') else None
        self.user_email = data.get('user_email') if data.get('user_email') else None
        self.image = data.get('image') if data.get('image') else None
        self.households = data.get('households') if data.get('households') else []
        meals = {}
        if data.get('meals'):
            for date, meals_list in data['meals'].items():
                for meal in meals_list:
                    if isinstance(meal,MealBoundaryWithIngredients):
                        meal = meal.__dict__
                    entity_meal = MealEntityWithIngredients(meal)
                    entity_meal.used_date = None
                    try:
                        meals[date].append(entity_meal.__dict__)
                    except KeyError:
                        meals[date] = [entity_meal.__dict__]

        self.meals = meals
        self.country = data.get('country') if data.get('country') else None
        self.state = data.get('state') if data.get('state') else None
