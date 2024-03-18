from fastapi import FastAPI
from routers.recipes import router as recipe_router

app = FastAPI()

app.include_router(recipe_router)
