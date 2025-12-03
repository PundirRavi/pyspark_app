# ingestion/sftp_ingestor.py

from sdk.ingestion.base import BaseIngestor, IngestionAction
from sdk.core.sftp.sftp_client import get_sftp_client
from sdk.core.utils.logger import logger
from typing import List
import os


class SFTPIngestor(BaseIngestor):
    def __init__(self):
        self.client = get_sftp_client()

    def list_files(self, action: IngestionAction) -> List[str]:
        try:
            files = self.client.listdir(action.source_path)
            logger.info(f"✅ Listed files in {action.source_path}: {files}")
            return files
        except Exception as e:
            logger.error(f"❌ Failed to list files: {e}")
            return []

    def download_file(self, action: IngestionAction) -> bool:
        try:
            self.client.get(action.source_path, action.destination_path)
            logger.info(f"✅ Downloaded {action.source_path} to {action.destination_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Download failed from {action.source_path} to {action.destination_path}: {e}")
            return False

    def upload_file(self, action: IngestionAction) -> bool:
        try:
            remote_dir = os.path.dirname(action.destination_path)
            if remote_dir not in self.client.listdir('.'):
                self.client.mkdir(remote_dir)
            self.client.put(action.source_path, action.destination_path)
            logger.info(f"✅ Uploaded {action.source_path} to {action.destination_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Upload failed from {action.source_path} to {action.destination_path}: {e}")
            return False
