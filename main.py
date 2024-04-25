from fastapi import FastAPI, APIRouter

from routers.recipes import router as recipes_router
from routers.user_household import router as user_household_router
app = FastAPI()

app.include_router(recipes_router)
app.include_router(user_household_router)