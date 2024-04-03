from fastapi import FastAPI, APIRouter

from routers.recipes import router as recipes_router
app = FastAPI()

app.include_router(recipes_router)
