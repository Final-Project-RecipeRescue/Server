import logging
from typing import List, Optional
from Data.Recipe_stepsEntity import Recipe_stepsEntity
from Data.recipe_entity import RecipeEntity, RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular
from Data.IngredientEntity import IngredientEntitySpoonacular
from routers_boundaries.recipe_boundary import RecipeBoundary
from routers_boundaries.IngredientBoundary import IngredientBoundary
from protocols.ServiceProtocol import Service
from DAL.recipes_db_connection import SpoonacularAPI, RecipesCRUD
from routers_boundaries.recipe_instructionsBoundary import recipe_instructionsBoundary, Step

logger = logging.getLogger("my_logger")


class RecipesService(Service):
    def __init__(self):
        self.spoonacular_instance = SpoonacularAPI().get_instance()
        self.recipeDB = RecipesCRUD()

    async def get_recipes_by_ingredients_lst(self, ingredients: List[str], missed_ingredients: bool) -> Optional[
        List[RecipeBoundary]]:
        try:
            recipes = await self.spoonacular_instance.find_recipes_by_ingredients(ingredients)
            if missed_ingredients:
                result = [self.toBoundaryRecipe(recipe) for recipe in recipes]
            else:
                result = [self.toBoundaryRecipe(recipe) for recipe in recipes if recipe.missed_ingredient_count == 0]
            for recipe in result:
                await self.add_recipe_to_mongoDB(recipe)
            return result if result else None
        except Exception as e:
            logger.error("In get_recipes_by_ingredients_lst func: %s", e)

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundary:
        try:
            recipe_id = int(recipe_id)
            recipe = self.recipeDB.get_recipe_by_id(str(recipe_id))
            if recipe is None:
                logger.info(f"Get from spoonacular recipe with recipe id {recipe_id}")
                recipe = self.toBoundaryRecipe(await (self.spoonacular_instance.find_recipe_by_id(recipe_id)))
                if recipe is not None:
                    await self.add_recipe_to_mongoDB(recipe)
            return recipe
        except Exception as e:
            logger.error("In get_recipe_by_id: %s", e)

    '''
    With this action we can get some recipes but it's not the most important because it takes a lot of points on the spoonacular server
    '''

    async def get_recipe_by_ids(self, recipe_ids: [str]) -> [RecipeBoundary]:
        try:
            ids = [int(id) for id in recipe_ids]
            return [self.toBoundaryRecipe(recipe)
                    for recipe in
                    (await (self.spoonacular_instance.find_recipe_by_ids(ids)))]
        except Exception as e:
            logger.error("In get_recipe_by_ids: %s", e)
            return None

    async def get_recipe_by_name(self, recipe_name) -> List[RecipeBoundary]:
        try:
            return [self.toBoundaryRecipe(recipe)
                    for recipe in
                    (await (self.spoonacular_instance.find_recipe_by_name(recipe_name)))]
        except Exception as e:
            logger.error("In get_recipe_by_name: %s", e)
            return None

    async def get_recipe_instructions(self, recipe_id: str):
        try:
            recipe_id = int(recipe_id)
            recipes_instructions = await (self.spoonacular_instance.get_analyzed_recipe_instructions(recipe_id))
            recipes_instructions_boundary = self.toBoundaryRecipeInstructions(recipes_instructions)
            return recipes_instructions_boundary
        except Exception as e:
            logger.error("In get_recipe_instructions: %s", e)
            return None

    async def add_recipe_to_mongoDB(self, recipe: RecipeBoundary):
        try:
            if not self.recipeDB.get_recipe_by_id(str(recipe.recipe_id)):
                await self.recipeDB.add_recipe(str(recipe.recipe_id), recipe)
            else:
                print(f"Recipe with id {recipe.recipe_id} already exists")
        except Exception as e:
            logger.error("In add_recipe_to_mongoDB: %s\n recipe_id = %d", e, recipe.recipe_id)

    def toBoundaryRecipeInstructions(self, recipes: List[Recipe_stepsEntity]) -> list[recipe_instructionsBoundary]:
        recipes_instructions = []
        for recipe in recipes:
            recipes_instructions.append(
                recipe_instructionsBoundary(
                    recipe.name,
                    [Step(int(step.number),
                          step.step,
                          int(step.length) if step.length is not None else 0,
                          [ingredient.name for ingredient in step.ingredients],
                          [equipment.name for equipment in step.equipments]
                          ) for step in recipe.steps])
            )
        return recipes_instructions

    def toBoundaryRecipe(self, recipeEntity: RecipeEntity) -> RecipeBoundary:
        recipeBoundary = RecipeBoundary(int(recipeEntity.id)
                                        , recipeEntity.title
                                        , []
                                        , recipeEntity.image)
        if isinstance(recipeEntity, RecipeEntityByIngredientSpoonacular):
            recipeBoundary.ingredients = ([self.toBoundryIngredient(ingredient)
                                           for ingredient in recipeEntity.missed_ingredients]
                                          + [self.toBoundryIngredient(ingredient)
                                             for ingredient in recipeEntity.used_ingredients])

        elif isinstance(recipeEntity, RecipeEntityByIDSpoonacular):
            recipeBoundary.ingredients = [self.toBoundryIngredient(ingredient) for ingredient in
                                          recipeEntity.extendedIngredients]
            recipeBoundary.summery = recipeEntity.summary
        return recipeBoundary

    def toBoundryIngredient(self, ingredient: IngredientEntitySpoonacular) -> IngredientBoundary:
        return IngredientBoundary(ingredient.id
                                  , ingredient.name
                                  , ingredient.amount
                                  , ingredient.unit_long if ingredient.unit_long is not None else ingredient.unit
                                  , None)
