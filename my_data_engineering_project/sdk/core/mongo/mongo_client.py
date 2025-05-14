from pydantic_settings import BaseSettings
from pydantic import Field
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ConfigurationError
from sdk.core.utils.logger import setup_logger  # optional: your existing logger

logger = setup_logger(__name__)

class MongoClientConfig(BaseSettings):
    host: str
    port: str = Field(default="27017")
    username: str
    password: str
    database: str
    auth_source: str
    ssl: bool = False
    connect_timeout_ms: int = 10000
    socket_timeout_ms: int = 10000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "MONGO_"
        populate_by_name = True

_config = MongoClientConfig()
_client: MongoClient = None

def _create_client() -> MongoClient:
    global _client
    if _client is None:
        uri = f"mongodb+srv://{_config.username}:{_config.password}@{_config.host}/{_config.database}?retryWrites=true&w=majority"
        try:
            _client = MongoClient(uri,
                                  tls=True,
                                  connectTimeoutMS=_config.connect_timeout_ms,
                                  socketTimeoutMS=_config.socket_timeout_ms)
            _client.admin.command('ping')
            logger.info("MongoDB connection successful")
        except (ConnectionFailure, ConfigurationError) as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    return _client

def get_collection(collection_name: str) -> Collection:
    """
    Returns a MongoDB collection object directly.
    """
    client = _create_client()
    return client[_config.database][collection_name]
