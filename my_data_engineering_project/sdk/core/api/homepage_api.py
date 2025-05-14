from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})