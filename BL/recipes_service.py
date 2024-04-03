from typing import List

from Data.recipe_entity import RecipeEntity, RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular
from Data.IngredientEntity import IngredientEntitySpoonacular
from routers_boundaries.recipe_boundary import RecipeBoundary
from routers_boundaries.Ingredient_boundary import ingredient_boundary
from protocols.ServiceProtocol import Service
from DAL.recipes_db_connection import SpoonacularAPI


class RecipesService(Service):
    def __init__(self):
        self.spoonacular_instance = SpoonacularAPI().get_instance()

    async def get_recipes_by_ingredients_lst(self, ingredients: List[str]) -> List[RecipeBoundary]:
        recipes = await (self.spoonacular_instance.find_recipes_by_ingredients(ingredients))
        try:
            return [self.toBoundryRecipe(recipe) for recipe in recipes]
        except Exception as e:
            print("In get_recipes_by_ingredients_lst func : ", e)
            return None

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundary:
        try:
            recipe_id = int(recipe_id)
            return self.toBoundryRecipe(await (self.spoonacular_instance.find_recipe_by_id(recipe_id)))
        except Exception as e:
            print("in get_recipe_by_id ", e)
            return None

    '''
    With this action we can get some recipes but it's not the most important because it takes a lot of points on the spoonacular server
    '''
    async def get_recipe_by_ids(self, recipe_ids: [str]) -> [RecipeBoundary]:
        try:
            ids = [int(id) for id in recipe_ids]
            return [self.toBoundryRecipe(recipe)
                    for recipe in
                    (await (self.spoonacular_instance.find_recipe_by_ids(ids)))]
        except Exception as e:
            print("in get_recipe_by_ids", e)
            return None

    async def get_recipe_by_name(self, recipe_name) -> List[RecipeBoundary]:
        try:
            return [self.toBoundryRecipe(recipe)
                    for recipe in
                    (await (self.spoonacular_instance.find_recipe_by_name(recipe_name)))]
        except Exception as e:
            print("in get_recipe_by_name ", e)
            return None

    def toBoundryRecipe(self, recipeEntity: RecipeEntity) -> RecipeBoundary:
        recipeBoundary = RecipeBoundary(id=int(recipeEntity.id)
                                        , recipe_name=recipeEntity.title
                                        , ingredients=[]
                                        , image_url=recipeEntity.image)
        print(recipeBoundary)
        if isinstance(recipeEntity, RecipeEntityByIngredientSpoonacular):
            recipeBoundary.ingredients = (
                    recipeEntity.missed_ingredients + recipeEntity.used_ingredients
            )
        elif isinstance(recipeEntity, RecipeEntityByIDSpoonacular):
            recipeBoundary.ingredients = recipeEntity.extendedIngredients
            recipeBoundary.summery = recipeEntity.summary
        return recipeBoundary

    def toBoundryIngredient(self, ingredient: IngredientEntitySpoonacular) -> ingredient_boundary:
        return ingredient_boundary(id=int(ingredient.id)
                                   , name=ingredient.name
                                   , amount=ingredient.amount
                                   , unit=ingredient.unit)
