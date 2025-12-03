from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from sdk.core.utils.logger import logger
import os

router = APIRouter()

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

class JobRequest(BaseModel):
    job_id: str
    job_name: str
    description: str
    source_type: str
    source_path: str
    destination_type: str
    destination_path: str
    file_type: str
    schedule: str
    enabled: bool
    created_at: str

@router.get("/create_job", response_class=HTMLResponse)
async def show_create_job_form(request: Request):
    return templates.TemplateResponse("create_job.html", {"request": request})

@router.post("/create_job")
async def create_job(
    job_name: str = Form(...),
    description: str = Form(""),
    source_type: str = Form(...),
    source_path: str = Form(...),
    destination_type: str = Form(...),
    destination_path: str = Form(...),
    file_type: str = Form(...),
    schedule: str = Form(...),
    enabled: str = Form(...)
):
    job_data = JobRequest(
        job_id=str(uuid4()),
        job_name=job_name,
        description=description,
        source_type=source_type,
        source_path=source_path,
        destination_type=destination_type,
        destination_path=destination_path,
        file_type=file_type,
        schedule=schedule,
        enabled=enabled.lower() == "true",
        created_at=datetime.utcnow().isoformat()
    )

    # You can log or store job_data in MongoDB here
    logger.info(f"📝 Ingestion job created: {job_data.model_dump()}")
    
    # Redirect to confirmation or job list
    return RedirectResponse(url="/create_job", status_code=303)
