# models/ingestion_job_model.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime,timezone

class IngestionJobModel(BaseModel):
    job_name: str = Field(..., example="load_patient_records")
    source_type: Literal["sftp", "aws_s3", "gcp_bucket", "azure_blob", "local", "api"]
    source_path: str
    destination_type: Literal["sftp", "aws_s3", "gcp_bucket", "azure_blob", "local"]
    destination_path: str
    file_type: Literal["csv", "excel", "json", "parquet", "hl7", "ccda", "fhir", "other"]
    schedule_type: Literal["one-time", "recurring"]
    schedule_time: Optional[datetime] = None  # For one-time jobs
    cron_expression: Optional[str] = None     # For recurring
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.timezone.utcnow)
    updated_at: datetime = Field(default_factory=datetime.timezone.utcnow)
