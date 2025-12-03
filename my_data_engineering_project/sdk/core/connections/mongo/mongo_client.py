

import sys
import os

# # Correct path: go up **three** levels to reach project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from sdk.core.utils.logger import logger


_client = None

def _create_client() -> MongoClient:
    global _client
    if _client is None:
        cfg = settings.mongo
        #uri = f"mongodb+srv://{cfg.username}:{cfg.password}@{cfg.host}/?retryWrites=true&w=majority&appName=DataStreaming"
        uri = f"mongodb+srv://ravikumar_db_user:QPhTvIDp0gE2yfY4@my-db.zwvwxzj.mongodb.net/?appName=my-db"

        try:
            _client = MongoClient(uri,
                                  server_api=ServerApi('1'))
            _client.admin.command('ping')
            logger.info("MongoDB connection successful")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    return _client

def get_collection(collection_name: str = None):
    client = _create_client()
    # collection_name = collection_name or settings.mongo.collection_user_auth
    return client
