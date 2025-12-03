# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

#MongoDB Class 
class MongoClientConfig(BaseSettings):
    host: str
    port: int = Field(default=27017)
    username: str
    password: str
    database: str
    collection: str
    auth_source: str = "admin"
    ssl: bool = False
    connect_timeout_ms: int = 10000
    socket_timeout_ms: int = 10000
    collection_user_auth: str

    class Config:
        env_prefix = "MONGO_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # forbid any extra env vars

#Snowflake Class
class SnowflakeConfig(BaseSettings):
    user:str
    password:str
    account:str
    warehouse: Optional[str]= None
    database: str
    schema:str
    role: Optional[str]=None

    class Config:
        env_prefix = "Snowflake_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

#SFTP Class
class SFTPConfig(BaseSettings):
    host: str
    port: int = Field(default=22)
    username: str
    password: str
    container_port: int = Field(default=22)
    source_path: str = Field(default="/home/sftp")
    remote_path: str = Field(default="/home/sftp")
    private_key_path: Optional[str] = None  # if you want to support private key auth
    timeout: int = 10

    class Config:
        env_prefix = "SFTP_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # forbid any extra env vars

#GCPClass
class GCPConfig(BaseSettings):
    # project_id: str 
    bucket_name: str 
    credentials_path: str 
    bigquery_dataset: str 
    bigquery_table: str
    meta_dataset: str = "metadata"

    class Config:
        env_prefix = "GCP_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

class Settings(BaseSettings):
    mongo: MongoClientConfig = MongoClientConfig()
    sftp: SFTPConfig = SFTPConfig()
    gcp: GCPConfig = GCPConfig()
    snowflake: SnowflakeConfig= SnowflakeConfig()
    
settings = Settings()
# print(settings.gcp)  # For debugging purposes
