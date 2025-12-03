from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sdk.core.connections.mongo import mongo_client
from datetime import datetime, timezone
from sdk.core.utils.logger import logger
from sdk.core.models.login_model import loginRequest
from fastapi import HTTPException, status
from sdk.configs.settings import settings
import bcrypt



import os

router = APIRouter()

logger.info("Initializing login API router...")

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Setup logger

logger.info(f"Templates directory set to: {TEMPLATE_DIR}")

# Middleware to handle exceptions
#router.()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    logger.info("Rendering login page")
    return templates.TemplateResponse("login.html", {"request": request})
    

@router.post("/login", response_class=HTMLResponse)
async def login_user(request: Request,
    form_data: loginRequest = Depends(loginRequest.as_form)):

    logger.info("Processing login request")
    """
    Handle the user login.
    Verifies the credentials from MongoDB and returns a response.
    """
    try:
        logger.info(f"recieved login request for user: {form_data.username}")
        #getting the mongo client object
        
        _client_obj = mongo_client.get_collection()

        # get/extract the collection object from the mongo client object 
        users_collection=_client_obj[settings.mongo.database][settings.mongo.collection]
        
            
        logger.info("connecting with mongo client collecton .......")

        # Query MongoDB to find the user by username
        user = users_collection.find_one({"username": form_data.username})
        # Log the login attempt
        logger.info(f"searching user in the mong db : {form_data.username}")

        if user is None:
            # Log the failed attempt
            logger.warning(f"Login failed: User {form_data.username} not found")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error_message": "User does not exist."},
                status_code=status.HTTP_401_UNAUTHORIZED
                )

        # Check password (Ensure you store the password securely, here we are doing it as plain for demo)
        # Verify the password (compare hashed password)
        if not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
            logger.warning(f"Login failed: Incorrect password for user '{form_data.username}'")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error_message": "Incorrect password."},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # If login is successful, log and return response
        logger.info(f"Login successful for username: {form_data.username}")

        # on Successfull Login update the last login time for the user.
        result = users_collection.update_one(
            {"username": form_data.username},
            {"$set": {"last_login": datetime.now(timezone.utc)
            }}  
            )
        
        # You can redirect the user to a homepage or dashboard
        return RedirectResponse(url="/home", status_code=303)

    except Exception as e:
        # Log any unexpected errors
        logger.error(f"An error occurred during login: {str(e)}")
        return templates.TemplateResponse(
                "login.html",
                {"request": request, "error_message": "Incorrect Credentials."},
                status_code=status.HTTP_401_UNAUTHORIZED
            )