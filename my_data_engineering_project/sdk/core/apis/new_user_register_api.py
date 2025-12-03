import bcrypt
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sdk.core.utils.logger import logger
from sdk.core.connections.mongo import mongo_client
from sdk.core.models.newuser_model import NewUserRegisterRequest
from pymongo.errors import DuplicateKeyError
from sdk.configs.settings import settings
import os

# Setup logger
router = APIRouter()

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

@router.get("/register", response_class=HTMLResponse)
def registration_page(request: Request,  success: str = None):
    logger.info("Rendering registration page")
    message = "Registration successful! You can now login." if success else None
    return templates.TemplateResponse("register.html", {"request": request, "success": message})
    


@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    form_data: NewUserRegisterRequest = Depends(NewUserRegisterRequest.as_form)
):
    logger.info(f"Received registration request for username: {form_data.username}")
    
    try:
        # Validate if user already exists with the same username,dob and gender
        _client_obj = mongo_client.get_collection()

        # get/extract the collection object from the mongo client object 
        users_collection=_client_obj[settings.mongo.database][settings.mongo.collection]
        
        # Check for existing user with same username, gender, and dob
        existing_user = users_collection.find_one({
            "username": form_data.username,
            "gender": form_data.gender,
            "date_of_birth": (lambda d: d if isinstance(d, str) else d.strftime("%Y-%m-%d"))(form_data.date_of_birth)  # Ensure this is stored/compared consistently
        })
        
        if existing_user:
            logger.warning("User already exists with same username, gender, and date of birth.")
            return templates.TemplateResponse("register.html", {
                "request": request,
                "error": "User already exists with the same username, gender, and date of birth."
            })
        
        # Hash the password before saving it
        hashed_password = bcrypt.hashpw(form_data.password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user dictionary
        user_data = form_data.model_dump()
        user_data["password"] = hashed_password.decode('utf-8')  # Store hashed password as string

        # Save the new user data into the database
        users_collection.insert_one(user_data)
        logger.info(f"User '{form_data.username}' registered successfully")

        # registration page with success message and login link
        response = RedirectResponse(url="/register?success=1", status_code=303)
        return response
    except DuplicateKeyError:
        logger.warning("Duplicate user registration attempt blocked by DB")
        return templates.TemplateResponse("register.html", {
        "request": request,
        "error": "User already exists with same name, gender, and date of birth."
        })

    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
