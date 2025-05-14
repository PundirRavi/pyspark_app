import bcrypt
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sdk.core.utils.logger import setup_logger
from sdk.core.mongo.mongo_client import get_collection
from sdk.core.models.newuser_model import NewUserRegisterRequest
import os

# Setup logger
logger = setup_logger(__name__)
router = APIRouter()

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/register", response_class=HTMLResponse)
def registration_page(request: Request):
    logger.info("Rendering registration page")
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    form_data: NewUserRegisterRequest = Depends(NewUserRegisterRequest.as_form)
):
    logger.info(f"Received registration request for username: {form_data.username}")
    
    try:
        # Hash the password before saving it
        hashed_password = bcrypt.hashpw(form_data.password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user dictionary
        user_data = form_data.dict()
        user_data["password"] = hashed_password.decode('utf-8')  # Store hashed password as string

        users_collection = get_collection("user_auth")

        # Check if the username already exists
        if users_collection.find_one({"username": form_data.username}):
            logger.warning(f"Registration failed: Username '{form_data.username}' already exists")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        # Save the new user data into the database
        users_collection.insert_one(user_data)
        logger.info(f"User '{form_data.username}' registered successfully")

        return templates.TemplateResponse("welcome_page.html", {"request": request, "username": form_data.username})

    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
