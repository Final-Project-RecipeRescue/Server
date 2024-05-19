from fastapi import FastAPI, APIRouter
import logging
from routers.recipes import router as recipes_router
from routers.user_household import router as user_household_router
from routers.ingredients import router as ingredients_router
app = FastAPI()

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
stream_handler = logging.FileHandler("server_log_file.log", mode='w')
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.info('Server is starting up')


app.include_router(recipes_router)
app.include_router(user_household_router)
app.include_router(ingredients_router)