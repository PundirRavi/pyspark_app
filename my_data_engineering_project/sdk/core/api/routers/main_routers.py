from fastapi import FastAPI

from sdk.core.api.welcome_page import router as welcome_router
from sdk.core.api.login_api import router as login_router
from sdk.core.api.new_user_register_api import router as new_user_register_router
from sdk.core.api.homepage_api import app as homepage_app
from fastapi.templating import Jinja2Templates
from sdk.core.utils.logger import setup_logger


import shutil
import os

logger=setup_logger(__name__)
# adding all apis in the routers
app = FastAPI()

logger.info("Starting FastAPI application...")
app.include_router(welcome_router)
logger.info("Welcome router included: /welcome")
app.include_router(login_router)
logger.info("Login router included: /login")
app.include_router(new_user_register_router)
logger.info("New user registration router included: /register")


