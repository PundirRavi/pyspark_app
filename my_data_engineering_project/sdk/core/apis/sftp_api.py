# routers/ingestion.py

from fastapi import APIRouter, Query, HTTPException
from sdk.ingestion.sftp_ingestor import SFTPIngestor
from sdk.ingestion.base import IngestionAction

router = APIRouter()

@router.get("/list_sftp_files")
async def list_sftp_files(path: str = Query('/', description="Remote directory path")):
    try:
        ingestor = SFTPIngestor()
        action = IngestionAction(source_path=path, destination_path="")
        files = ingestor.list_files(action)
        # If you have a close method for client, call here e.g. ingestor.client.close()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {e}")
