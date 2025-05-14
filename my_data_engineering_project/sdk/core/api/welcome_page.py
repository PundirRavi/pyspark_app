from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from sdk.core.utils.logger import setup_logger

router = APIRouter()

# Setup logger
logger = setup_logger(__name__)

logger.info("Starting FastAPI application...")
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
print(TEMPLATE_DIR)
templates = Jinja2Templates(directory=TEMPLATE_DIR)

logger.info(f"Templates directory set to: {TEMPLATE_DIR}")

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    logger.info("Rendering home page")
    return templates.TemplateResponse("welcome_page.html", {"request": request})
