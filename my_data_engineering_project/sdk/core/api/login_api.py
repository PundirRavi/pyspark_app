from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sdk.core.mongo.mongo_client import get_collection

from sdk.core.middleware import exception_handler
from sdk.core.utils.logger import setup_logger
from sdk.core.mongo import mongo_client
from sdk.core.models.login_model import loginRequest
from fastapi import HTTPException, status
import bcrypt



import os

logger = setup_logger(__name__)

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
        #getting the collection object
        
        users_collection = get_collection("user_auth")
        
            
        logger.info("connecting with mongo client collecton .......")

        # Query MongoDB to find the user by username
        user = users_collection.find_one({"username": form_data.username})
        # Log the login attempt
        logger.info(f"searching user in the mong db : {form_data.username}")
        if user is None:
            # Log the failed attempt
            logger.warning(f"Login failed: User {form_data.username} not found")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # Check password (Ensure you store the password securely, here we are doing it as plain for demo)
        # Verify the password (compare hashed password)
        if not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
            logger.warning(f"Login failed: Incorrect password for user '{form_data.username}'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        # If login is successful, log and return response
        logger.info(f"Login successful for username: {form_data.username}")
        
        # You can redirect the user to a homepage or dashboard
        return templates.TemplateResponse("home_page.html", {"request": request, "username": form_data.username})

    except Exception as e:
        # Log any unexpected errors
        logger.error(f"An error occurred during login: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")