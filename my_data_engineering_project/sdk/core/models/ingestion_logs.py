# models/ingestion_log.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class IngestionLog(BaseModel):
    service: str
    action: str
    source_path: str
    destination_path: str
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict] = {}
    error: Optional[str] = None
