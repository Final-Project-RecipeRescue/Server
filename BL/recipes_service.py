import logging
from datetime import datetime
from typing import List, Optional
from Data.IngredientEntity import IngredientEntity
from Data.Recipe_stepsEntity import Recipe_stepsEntity
from Data.recipe_entity import RecipeEntity, RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.recipe_boundary import RecipeBoundary
from protocols.ServiceProtocol import Service
from DAL.recipes_db_connection import SpoonacularAPI, RecipesCRUD, RecipesInstructionsCRUD
from routers_boundaries.recipe_instructionsBoundary import recipe_instructionsBoundary, Step

logger = logging.getLogger("my_logger")
date_format = "%Y-%m-%d"


def to_ingredient_boundary(ingredient: IngredientEntity) -> IngredientBoundary:
    return IngredientBoundary(
        ingredient.id,
        ingredient.name,
        ingredient.amount,
        ingredient.unit,
        None)


def toBoundaryRecipe(recipeEntity: RecipeEntity) -> RecipeBoundary:
    logger.info(f"In toBoundaryRecipe get Recipe Entity : {recipeEntity.__dict__}")
    recipeBoundary = RecipeBoundary(int(recipeEntity.id)
                                    , recipeEntity.title
                                    , []
                                    , recipeEntity.image)
    if isinstance(recipeEntity, RecipeEntityByIngredientSpoonacular):
        recipeBoundary.ingredients = ([to_ingredient_boundary(ingredient)
                                       for ingredient in recipeEntity.missed_ingredients]
                                      + [to_ingredient_boundary(ingredient)
                                         for ingredient in recipeEntity.used_ingredients])

    elif isinstance(recipeEntity, RecipeEntityByIDSpoonacular):
        recipeBoundary.ingredients = [to_ingredient_boundary(ingredient) for ingredient in
                                      recipeEntity.extendedIngredients]
        recipeBoundary.summery = recipeEntity.summary
    logger.info(f"Success to do toBoundaryRecipe")
    return recipeBoundary


def toBoundaryRecipeInstructions(recipe: Recipe_stepsEntity) -> recipe_instructionsBoundary:
    return recipe_instructionsBoundary(
        recipe.name if recipe.name is not None else "",
        [Step(
            step.number,
            step.step,
            step.length.number if step.length is not None else 0,
            [{ingredient.name: ingredient.image} for ingredient in step.ingredients],
            [{equipment.name: equipment.image} for equipment in step.equipments]
        ) for step in recipe.steps]
    )


class RecipesService(Service):
    def __init__(self):
        self.spoonacular_instance = SpoonacularAPI().get_instance()
        self.recipeDB = RecipesCRUD()
        self.recipesInstructionsCRUD = RecipesInstructionsCRUD()

    async def get_recipes_by_ingredients_lst(self, ingredients: List[str], missed_ingredients: bool) -> Optional[
        List[RecipeBoundary]]:
        try:
            recipes = await self.spoonacular_instance.find_recipes_by_ingredients(ingredients)
            if missed_ingredients:
                result = [await self.add_recipe_to_mongoDB(toBoundaryRecipe(recipe)) for recipe in recipes]
            else:
                result = [await self.add_recipe_to_mongoDB(toBoundaryRecipe(recipe)) for recipe in recipes if
                          recipe.missed_ingredient_count == 0]
            return result if result else None
        except Exception as e:
            logger.error("In get_recipes_by_ingredients_lst func: %s", e)

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundary:
        try:
            recipe_id = int(recipe_id)
            recipe = await self.recipeDB.get_recipe_by_id(str(recipe_id))
            if recipe is None:
                logger.info(f"Get from spoonacular recipe with recipe id {recipe_id}")
                recipe = toBoundaryRecipe(await (self.spoonacular_instance.find_recipe_by_id(recipe_id)))
                if recipe is not None:
                    await self.add_recipe_to_mongoDB(recipe)
            return recipe
        except Exception as e:
            logger.error("In get_recipe_by_id: %s", e)

    async def get_recipe_by_name(self, recipe_name) -> List[RecipeBoundary]:
        try:
            return [toBoundaryRecipe(recipe)
                    for recipe in
                    (await (self.spoonacular_instance.find_recipe_by_name(recipe_name)))]
        except Exception as e:
            logger.error("In get_recipe_by_name: %s", e)
            return None

    async def get_recipe_instructions(self, recipe_id: str):
        try:
            recipe_id = int(recipe_id)
            instructions = self.recipesInstructionsCRUD.get_recipe_instructions(str(recipe_id))
            if instructions is None:
                instructions = await (self.spoonacular_instance.get_analyzed_recipe_instructions(recipe_id))
                if instructions is not None:
                    logger.info("get recipe instructions from spoonacular!")
                    try:
                        self.recipesInstructionsCRUD.add_recipe_instructions(str(recipe_id), instructions)
                    except Exception as e:
                        logger.error("Dont add recipe_instructions: %s to mongo error : %s", recipe_id,e)
            else:
                logger.info("get recipe instructions from mongo!")

            recipes_instructions_boundary = [toBoundaryRecipeInstructions(recipe) for recipe in
                                             instructions]
            return recipes_instructions_boundary
        except Exception as e:
            logger.error("In get_recipe_instructions: %s", e)
            return None

    async def add_recipe_to_mongoDB(self, recipe: RecipeBoundary) -> RecipeBoundary:
        try:
            existing_recipe = await self.recipeDB.get_recipe_by_id(str(recipe.recipe_id))
            if existing_recipe is None:
                for ingredient in recipe.ingredients:
                    if ingredient.unit != 'g' and ingredient.unit != 'gram':
                        ingredient.amount = await self.spoonacular_instance.convertIngredientAmountToGrams(
                            ingredient.name, ingredient.amount, ingredient.unit)
                        ingredient.unit = "gram"
                self.recipeDB.add_recipe(str(recipe.recipe_id), recipe)
                logger.info(f"Recipe {recipe.recipe_id} added to mongoDB")
            else:
                recipe = existing_recipe
                logger.info(f"Recipe with id {recipe.recipe_id} already exists")
            return recipe
        except Exception as e:
            logger.error("In add_recipe_to_mongoDB: %s\n recipe_id = %d", e, recipe.recipe_id)

