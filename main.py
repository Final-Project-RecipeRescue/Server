from fastapi import FastAPI
import logging
from routers.recipes import router as recipes_router
from routers.user_household import router as user_household_router
from routers.ingredients import router as ingredients_router

app = FastAPI()

# Create a logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = logging.FileHandler("server_log_file.log", mode='w')
console_handler = logging.StreamHandler()

# Create formatters and add them to the handlers
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_formatter)
console_handler.setFormatter(log_formatter)
# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('Server is starting up')

# Include routers
app.include_router(recipes_router)
app.include_router(user_household_router)
app.include_router(ingredients_router)
