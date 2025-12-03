# sdk/utils/sftp_client.py
import paramiko
import os
import sys
# Get the absolute path to your project root folder (assuming this file is inside sdk/core/mongo/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from sdk.configs.settings import settings
from sdk.core.utils.logger import logger

def get_sftp_client():
    config = settings.sftp
    try:
        transport = paramiko.Transport((config.host, config.port))
        transport.connect(username=config.username, password=config.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        logger.info("✅ SFTP connection established", extra={"service": "sftp", "status": "success"})
        return sftp
    except Exception as e:
        logger.error(f"❌ SFTP connection failed: {e}")
        raise e
