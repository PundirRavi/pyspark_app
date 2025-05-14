from .base import BaseIngestor
from core.models.connector_model import SFTPConnector

import paramiko
import os

class SFTPIngestor(BaseIngestor):
    def __init__(self, config: SFTPConnector):
        """
        Initialize the SFTPIngestor with the provided configuration.

        Args:
            config (SFTPConnector): Configuration for the SFTP connector.
        """
        self.config = config

    def load_file(self, path: str):
        transport = paramiko.Transport((self.config.host, self.config.port))
        transport.connect(username=self.config.username, password=self.config.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
