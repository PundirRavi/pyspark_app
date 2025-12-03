# routes/ingestion_jobs.py

from fastapi import APIRouter, HTTPException
from models.ingestion_job_model import IngestionJobModel
from sdk.core.connections.mongo import mongo_client

router = APIRouter()
collection = mongo_client.get_collection("ingestion_jobs")

@router.post("/create_job")
async def create_job(job: IngestionJobModel):
    try:
        existing = collection.find_one({"job_name": job.job_name})
        if existing:
            raise HTTPException(status_code=400, detail="Job name already exists.")
        collection.insert_one(job.dict())
        return {"message": "✅ Ingestion job created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating job: {str(e)}")
