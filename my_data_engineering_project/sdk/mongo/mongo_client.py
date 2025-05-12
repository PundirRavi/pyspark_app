from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv
import os

class MongoClientConfig(BaseModel):
    """
    Configuration for MongoDB client.
    """
    host: str = "localhost"
    port: int = 27017
    username: str = None
    password: str = None
    database: str = "test"
    auth_source: str = "admin"
    ssl: bool = False
    connect_timeout_ms: int = 10000
    socket_timeout_ms: int = 10000

def load_env_variables():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()
    return {
        "MONGO_HOST": os.getenv("MONGO_HOST", "localhost"),
        "MONGO_PORT": int(os.getenv("MONGO_PORT", 27017)),
        "MONGO_USERNAME": os.getenv("MONGO_USERNAME"),
        "MONGO_PASSWORD": os.getenv("MONGO_PASSWORD"),
        "MONGO_DATABASE": os.getenv("MONGO_DATABASE", "test"),
        "MONGO_AUTH_SOURCE": os.getenv("MONGO_AUTH_SOURCE", "admin"),
        "MONGO_SSL": os.getenv("MONGO_SSL", "false").lower() == 'true',
        "MONGO_CONNECT_TIMEOUT_MS": int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", 10000)),
        "MONGO_SOCKET_TIMEOUT_MS": int(os.getenv("MONGO_SOCKET_TIMEOUT_MS", 10000))
    }