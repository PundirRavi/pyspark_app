from fastapi import Form
import bcrypt
from fastapi import APIRouter, Request,status
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sdk.core.connections.mongo import mongo_client
from sdk.core.utils.logger import logger
from datetime import datetime, timezone
import os


router = APIRouter()

logger.info("Initializing login API router...")

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/reset_password", response_class=HTMLResponse)
async def reset_password_form(request: Request, username: str):
    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "username": username}
    )


@router.post("/reset_password")
async def reset_password_submit(
    request: Request,
    username: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    try:
        if new_password != confirm_password:
            return templates.TemplateResponse(
                "reset_password.html",
                {"request": request, "username": username, "error": "Passwords do not match."}
            )

        users_collection = mongo_client.get_collection()
        result = users_collection.update_one(
            {"username": username},
            {"$set": {"password": bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "updated_on": datetime.now(timezone.utc)
        }}  # In real apps: hash the password
        )

        if result.modified_count == 0:
            return templates.TemplateResponse(
                "reset_password.html",
                {"request": request, "username": username, "error": "Failed to update password."}
            )

        return RedirectResponse(
            url="/login?message=Password updated successfully. Please login.",
            status_code=status.HTTP_303_SEE_OTHER
            )

    except Exception as e:
        logger.error(f"Reset password error: {str(e)}")
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "username": username, "error": "Internal Server Error"}
        )
