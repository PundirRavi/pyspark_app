# ingestion/gcp_ingestor.py

from ingestion.base import IngestionAction, BaseBigQueryIngestor
from sdk.google_client.gcp_client import get_gcp_client
from google.cloud import storage, bigquery
from sdk.configs.settings import settings
from sdk.core.utils.logger import logger
from typing import List, Optional
import os


class GCPIngestor(BaseBigQueryIngestor):
    def __init__(self):
        self.bigquery_client = get_gcp_client()
        self.gcs_client = storage.Client.from_service_account_json(settings.gcp.credentials_path)
        self.bucket = self.gcs_client.bucket(settings.gcp.bucket_name)
        self.project_id = self.bigquery_client.project

    def list_files(self, action: IngestionAction) -> List[str]:
        logger.info(f"🔍 Listing files in GCS path: {action.source_path}")
        try:
            blobs = self.bucket.list_blobs(prefix=action.source_path)
            file_list = [blob.name for blob in blobs]
            logger.info(f"✅ Found {len(file_list)} files.")
            return file_list
        except Exception as e:
            logger.error(f"❌ Failed to list files: {e}")
            return []

    def download_file(self, action: IngestionAction) -> bool:
        try:
            blob = self.bucket.blob(action.source_path)
            os.makedirs(os.path.dirname(action.destination_path), exist_ok=True)
            blob.download_to_filename(action.destination_path)
            logger.info(f"✅ File downloaded to {action.destination_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to download file from GCS: {e}")
            return False

    def upload_file(self, action: IngestionAction) -> bool:
        try:
            blob = self.bucket.blob(action.destination_path)
            blob.upload_from_filename(action.source_path)
            logger.info(f"✅ File uploaded to GCS at {action.destination_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to upload file to GCS: {e}")
            return False

    def ingest_to_bigquery(self, action: IngestionAction, schema: Optional[object] = None) -> bool:
        try:
            uri = f"gs://{settings.gcp.bucket_name}/{action.source_path}"
            table_id = f"{self.project_id}.{settings.gcp.bigquery_dataset}.{settings.gcp.bigquery_table}"

            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON if uri.endswith(".json") else bigquery.SourceFormat.CSV,
                autodetect=schema is None,
                skip_leading_rows=1 if uri.endswith(".csv") else 0,
            )

            if schema:
                job_config.schema = schema

            load_job = self.bigquery_client.load_table_from_uri(uri, table_id, job_config=job_config)
            load_job.result()

            logger.info(f"✅ Successfully ingested data from {uri} to BigQuery table: {table_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to ingest to BigQuery: {e}")
            return False
