from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field

class IngestionAction(BaseModel):
    source_path: str
    destination_path: str
    action: str  # e.g., "upload", "download", "list"
    status: str  # "success" or "failure"
    timestamp: Optional[str] = None
    details: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)

class BaseIngestor(ABC):
    @abstractmethod
    def list_files(self, action: IngestionAction) -> List[str]:
        pass

    @abstractmethod
    def download_file(self, action: IngestionAction) -> bool:
        pass

    @abstractmethod
    def upload_file(self, action: IngestionAction) -> bool:
        pass


class BaseBigQueryIngestor(BaseIngestor):
    @abstractmethod
    def ingest_to_bigquery(self, action: IngestionAction, schema: Optional[object] = None) -> bool:
        """
        Ingests data from a source (usually GCS file) into BigQuery.
        """
        pass