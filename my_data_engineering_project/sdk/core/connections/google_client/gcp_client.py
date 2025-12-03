# core/gcp/gcp_client.py

# import sys
# import os

# # Correct path: go up **three** levels to reach project root
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google.cloud import bigquery
from google.oauth2 import service_account
from sdk.configs.settings import settings
from sdk.core.utils.logger import logger  # Assumes logger is set up in utils/logger.py

from google.api_core.exceptions import GoogleAPICallError


def get_gcp_client() -> bigquery.Client:
    """
    Creates and returns a BigQuery client using service account credentials.
    """
    try:
        logger.info("Initializing BigQuery client...")

        credentials = service_account.Credentials.from_service_account_file(
            settings.gcp.credentials_path
        )

        client = bigquery.Client(
            credentials=credentials,
            project=credentials.project_id
        )

        logger.info("✅ BigQuery client initialized successfully.")
        return client

    except FileNotFoundError as e:
        logger.error(f"❌ Credentials file not found at: {settings.gcp.credentials_path}")
        raise e

    except GoogleAPICallError as e:
        logger.error(f"❌ Google API call failed: {str(e)}")
        raise e

    except Exception as e:
        logger.exception(f"❌ Unexpected error while initializing BigQuery client: {str(e)}")
        raise e
