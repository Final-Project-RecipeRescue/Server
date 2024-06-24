from Data.MealEntity import MealEntity
from routers_boundaries.MealBoundary import MealBoundary


class UserEntity:
    def __init__(self, data):
        self.first_name = data.get('first_name') if data.get('first_name') else None
        self.last_name = data.get('last_name') if data.get('last_name') else None
        self.user_email = data.get('user_email') if data.get('user_email') else None
        self.image = data.get('image') if data.get('image') else None
        self.households = data.get('households') if data.get('households') else []
        self.country = data.get('country') if data.get('country') else None
        self.state = data.get('state') if data.get('state') else None
        self.meals = data.get('meals') if data.get('meals') else {}


class UserEntityWithGasPollution(UserEntity):
    def __init__(self, data):
        super().__init__(data)
        self.sum_gas_pollution = data.get('sum_gas_pollution', {str, float}) if data.get('sum_gas_pollution') else {}
