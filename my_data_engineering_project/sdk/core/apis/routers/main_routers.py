from fastapi import FastAPI

# from sdk.core.apis.welcome_page import router as welcome_router
# from sdk.core.apis.login_api import router as login_router
# from sdk.core.apis.new_user_register_api import router as new_user_register_router
# from sdk.core.apis.forgot_password_api import router as forgot_password_router
# from sdk.core.apis.reset_password_api import router as reset_password_router
from sdk.core.apis.deploy_schema import router as deploy_schema_router

from sdk.core.apis.homepage_api import app as homepage_app

# from sdk.core.apis.sftp_api import router as sftp_router
from fastapi.templating import Jinja2Templates
from sdk.core.utils.logger import logger


import shutil
import os

# adding all apis in the routers
app = FastAPI()

# logger.info("Starting FastAPI application...")
# app.include_router(welcome_router)
# logger.info("Welcome router included: /welcome")

# app.include_router(login_router)
# logger.info("Login router included: /login")

# # Include the homepage router
# app.include_router(homepage_app)
# logger.info("Homepage router included: /home")

# #Include the new user registration router

# app.include_router(new_user_register_router)
# logger.info("New user registration router included: /register")

# app.include_router(forgot_password_router)
# logger.info("Forgot password router included: /forgot_password")

# app.include_router(reset_password_router)
# logger.info("Reset password router included: /reset_password")

app.include_router(deploy_schema_router)
logger.info("deploy schema router included: /deploy-schema")

# app.include_router(sftp_router,prefix="/sftp", tags=["SFTP"])
# logger.info("SFTP router included: /sftp")


