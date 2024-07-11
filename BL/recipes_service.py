import logging
from typing import List, Optional
from BL.ingredient_service import IngredientService
from Data.IngredientEntity import IngredientEntity
from Data.Recipe_stepsEntity import Recipe_stepsEntity
from Data.recipe_entity import RecipeEntity, RecipeEntityByIngredientSpoonacular, RecipeEntityByIDSpoonacular
from routers_boundaries.IngredientBoundary import IngredientBoundary
from routers_boundaries.recipe_boundary import RecipeBoundary, RecipeBoundaryWithGasPollution
from protocols.ServiceProtocol import Service
from DAL.recipes_db_connection import SpoonacularAPI, RecipesCRUD, RecipesInstructionsCRUD
from routers_boundaries.recipe_instructionsBoundary import recipe_instructionsBoundary, Step
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger("my_logger")
date_format = "%Y-%m-%d"
spoonacular_instance = SpoonacularAPI().get_instance()
ingredientService = IngredientService()


def to_ingredient_boundary(ingredient: IngredientEntity) -> IngredientBoundary:
    return IngredientBoundary(
        ingredient.id,
        ingredient.name,
        ingredient.amount,
        ingredient.unit,
        None)


async def convert_ingredient_unit_to_gram(ingredient: IngredientBoundary) -> IngredientBoundary:
    if ingredient.unit.lower() not in ['g', 'gram']:
        logger.info(f"Convert unit of ingredient \'{ingredient.name}\' from \'{ingredient.unit}\' to gram")
        amount = await spoonacular_instance.convertIngredientAmountToGrams(
            ingredient.name, ingredient.amount, ingredient.unit)
        if amount:
            logger.info(f"Successful converted unit of ingredient \'{ingredient.name}\' from {ingredient.amount} on {ingredient.unit} to {amount} on gram")
            ingredient.amount = amount
        ingredient.unit = 'gram'  # Assuming conversion sets unit to grams
    return ingredient


def calc_co2_emission_for_ingredient(ingredient):
    co2_emissions = 0
    try:
        '''
        Search by ID
        '''
        ing_data = ingredientService.get_ingredient_by_id(ingredient.ingredient_id)
        co2_emissions = (ingredient.amount / 100) * ing_data.gCO2e_per_100g
    except Exception:
        try:
            '''
            Search by name if the ID is not found
            '''
            ing_data = ingredientService.search_ingredient_by_name(ingredient.name)
            co2_emissions = (ingredient.amount / 100) * ing_data.gCO2e_per_100g
        except Exception:
            try:
                '''
                Search by autocomplete
                If we find ingredient with the same name we
                will take him but if not then we will take the first one that appears
                '''
                ingredients_data = ingredientService.autocomplete_by_ingredient_name(ingredient.name)
                ing_data = ingredients_data[0]
                for ing in ingredients_data:
                    if ing.name.lower() == ingredient.name.lower():
                        ing_data = ing
                co2_emissions = (ingredient.amount / 100) * ing_data.gCO2e_per_100g
            except Exception:
                logger.error(f"fail to find co2 for ingredient: {ingredient.name} ing_id: {ingredient.ingredient_id}")
    return co2_emissions


def calc_cos_gas_pollution(recipe: RecipeBoundary) -> RecipeBoundaryWithGasPollution:
    # logger.info(f"recipe {recipe.recipe_name} calc gas co2")
    sumGas = 0

    # Use ThreadPoolExecutor to parallelize ingredient processing
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(calc_co2_emission_for_ingredient, ingredient) for ingredient in recipe.ingredients]

        # Only the main thread will collect and sum the results
        for future in as_completed(futures):
            sumGas += future.result()

    # Create the result object
    recipeBoundaryWithGasPollution = RecipeBoundaryWithGasPollution(
        recipe,
        {}
    )
    recipeBoundaryWithGasPollution.sumGasPollution["CO2"] = sumGas

    return recipeBoundaryWithGasPollution


async def toBoundaryRecipe(recipeEntity: RecipeEntity) -> RecipeBoundary:
    # logger.info(f"In toBoundaryRecipe get Recipe Entity : {recipeEntity.__dict__}")
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
    recipeBoundary.ingredients = [await convert_ingredient_unit_to_gram(ingredient) for ingredient in
                                  recipeBoundary.ingredients]
    # logger.info(f"Success to do toBoundaryRecipe")
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


import time


class RecipesService(Service):
    def __init__(self):
        self.recipeDB = RecipesCRUD()
        self.recipesInstructionsCRUD = RecipesInstructionsCRUD()

    async def add_missing_recipes_to_mongo(self, recipes: [RecipeEntityByIngredientSpoonacular]):
        for recipe in recipes:
            recipe_from_mongo = await self.recipeDB.get_recipe_by_id(str(recipe.id))
            if recipe_from_mongo is None:
                logger.info(f"not exist in mongo data: {recipe.title}")
                await self.add_recipe_to_mongoDB(await toBoundaryRecipe(recipe))
                logger.info(f"recipe {recipe.title} added to mongo data")

    async def filter_and_calc_pollution(self, recipes: list[RecipeEntityByIngredientSpoonacular], missed_ingredients) -> \
            List[RecipeBoundaryWithGasPollution]:
        result: [RecipeBoundaryWithGasPollution] = []

        with ThreadPoolExecutor() as executor:
            futures = []
            for recipe in recipes:
                if missed_ingredients or recipe.missed_ingredient_count == 0:
                    futures.append(executor.submit(
                        calc_cos_gas_pollution, await self.recipeDB.get_recipe_by_id(str(recipe.id))
                    ))
            for future in as_completed(futures):
                result.append(future.result())
        return result

    async def get_recipes_by_ingredients_lst(self, ingredients: List[str], missed_ingredients: bool) \
            -> Optional[List[RecipeBoundaryWithGasPollution]]:
        try:
            recipes = await spoonacular_instance.find_recipes_by_ingredients(ingredients)
            await self.add_missing_recipes_to_mongo(recipes)
            result = await self.filter_and_calc_pollution(recipes, missed_ingredients)
            result.sort(key=lambda r: r.composite_score(1, 0), reverse=True)
            return result
        except Exception as e:
            logger.error("In get_recipes_by_ingredients_lst func: %s", e)

    async def get_recipe_by_id(self, recipe_id: str) -> RecipeBoundaryWithGasPollution:
        try:
            recipe_id = int(recipe_id)
            recipe = await self.recipeDB.get_recipe_by_id(str(recipe_id))
            if recipe is None:
                logger.info(f"Get from spoonacular recipe with recipe id {recipe_id}")
                recipe = await toBoundaryRecipe(await (spoonacular_instance.find_recipe_by_id(recipe_id)))
                if recipe is not None:
                    await self.add_recipe_to_mongoDB(recipe)
            if isinstance(recipe, RecipeBoundary):
                return calc_cos_gas_pollution(recipe)
            else:
                raise Exception
        except Exception as e:
            logger.error("In get_recipe_by_id: %s", e)

    async def get_recipe_by_name(self, recipe_name) -> List[RecipeBoundaryWithGasPollution]:
        rv = []
        try:
            recipes = await spoonacular_instance.find_recipe_by_name(recipe_name)
            for recipe in recipes:
                try:
                    recipe_t = await self.get_recipe_by_id(recipe.id)
                    rv.append(recipe_t)
                except Exception:
                    pass
            return rv
        except Exception as e:
            logger.error("In get_recipe_by_name: %s", e)

    async def get_recipe_instructions(self, recipe_id: str):
        try:
            recipe_id = int(recipe_id)
            instructions = self.recipesInstructionsCRUD.get_recipe_instructions(str(recipe_id))
            if instructions is None:
                instructions = await (spoonacular_instance.get_analyzed_recipe_instructions(recipe_id))
                if instructions is not None:
                    logger.info("get recipe instructions from spoonacular!")
                    try:
                        self.recipesInstructionsCRUD.add_recipe_instructions(str(recipe_id), instructions)
                    except Exception as e:
                        logger.error("Dont add recipe_instructions: %s to mongo error : %s", recipe_id, e)
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
                self.recipeDB.add_recipe(str(recipe.recipe_id), recipe)
                logger.info(f"Recipe {recipe.recipe_id} added to mongoDB")
            else:
                recipe = existing_recipe
                logger.info(f"Recipe with id {recipe.recipe_id} already exists")
            return recipe
        except Exception as e:
            logger.error("In add_recipe_to_mongoDB: %s\n recipe_id = %d", e, recipe.recipe_id)
