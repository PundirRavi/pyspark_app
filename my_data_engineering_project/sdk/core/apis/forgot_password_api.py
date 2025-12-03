from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sdk.core.models.forgot_password_model import forgotPasswordRequest
from sdk.core.connections.mongo.mongo_client import get_collection
from sdk.core.utils.logger import logger
from datetime import datetime
import os


router = APIRouter()

logger.info("Initializing login API router...")

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/forgot_password", response_class=HTMLResponse)
async def forgot_password_form(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})



@router.post("/forgot_password")
async def forgot_password_submit(
    request: Request,
    form_data: forgotPasswordRequest = Depends(forgotPasswordRequest.as_form)
):
    try:
        logger.info("Processing forgot password request")

        users_collection = get_collection()
        user = users_collection.find_one({
            "username": form_data.username,
            "gender": form_data.gender,
            "date_of_birth": (lambda d: d if isinstance(d, str) else d.strftime("%Y-%m-%d"))(form_data.date_of_birth),
        })

        if not user:
            logger.warning(f"Password reset failed for username: {form_data.username}")
            return templates.TemplateResponse(
                "forgot_password.html",
                {"request": request, "error": "User verification failed."},
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Simulate success (you could redirect to a reset password page or email a link)
        logger.info(f"Password reset request verified for {form_data.username}")
        return RedirectResponse(
            url=f"/reset_password?username={form_data.username}",
            status_code=status.HTTP_303_SEE_OTHER
        )

    except Exception as e:
        logger.error(f"Forgot password error: {str(e)}")
        return templates.TemplateResponse(
            "forgot_password.html",
            {"request": request, "error": "Internal Server Error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
