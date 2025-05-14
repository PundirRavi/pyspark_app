from pydantic import BaseModel, HttpUrl, Field, BaseSettings
from typing import Optional, Literal

class SFTPConnector(BaseSettings):
    """
    Configuration for SFTP connector.
    """
    host: str = Field(..., description="SFTP server hostname or IP address")
    port: int = Field(22, description="SFTP server port")
    username: str = Field(..., description="Username for SFTP authentication")
    password: str = Field(..., description="Password for SFTP authentication")
    remote_path: str = Field(..., description="Remote path on the SFTP server")
    local_path: str = Field(..., description="Local path to save files")
    protocol: Literal["sftp"] = "sftp"  # Fixed value for SFTP

    class Config:
        env_prefix = ".env"  # Prefix for environment variables
        env_file = ".env"  # Path to the environment file

class S3Connector(BaseModel):
    """
    Configuration for S3 connector.
    """
    access_key: str = Field(..., description="AWS access key")
    secret_key: str = Field(..., description="AWS secret key")  
    bucket_name: str = Field(..., description="S3 bucket name")
    region: str = Field(..., description="AWS region")
    key: str = Field(..., description="S3 object key")
    local_path: str = Field(..., description="Local path to save files")


class HTTPConnector(BaseModel):
    """
    Configuration for HTTP connector.
    """
    url: HttpUrl = Field(..., description="URL to fetch data from")
    method: Literal["GET", "POST"] = Field("GET", description="HTTP method to use")
    headers: Optional[dict] = Field(None, description="HTTP headers to include in the request")
    params: Optional[dict] = Field(None, description="Query parameters to include in the request")
    data: Optional[dict] = Field(None, description="Data to send in the request body")

class GCPConnector(BaseModel):
    """
    Configuration for GCP connector.
    """
    project_id: str = Field(..., description="GCP project ID")
    bucket_name: str = Field(..., description="GCS bucket name")
    object_name: str = Field(..., description="GCS object name")
    local_path: str = Field(..., description="Local path to save files")
    blob_name: str = Field(..., description="GCS blob name")
    credentials_path: str = Field(..., description="Path to GCP credentials JSON file")

class AzureConnector(BaseModel):
    """
    Configuration for Azure connector.
    """
    account_name: str = Field(..., description="Azure Storage account name")
    account_key: str = Field(..., description="Azure Storage account key")
    container_name: str = Field(..., description="Azure Blob Storage container name")
    blob_name: str = Field(..., description="Blob name in Azure Blob Storage")
    local_path: str = Field(..., description="Local path to save files")

class FTPConnector(BaseModel):
    """
    Configuration for FTP connector.
    """
    host: str = Field(..., description="FTP server hostname or IP address")
    port: int = Field(21, description="FTP server port")
    username: str = Field(..., description="Username for FTP authentication")
    password: str = Field(..., description="Password for FTP authentication")
    remote_path: str = Field(..., description="Remote path on the FTP server")
    local_path: str = Field(..., description="Local path to save files")

class LoadRequest(BaseModel):
    source_type: Literal["sftp", "s3", "http", "gcp", "azure", "ftp"] = Field(..., description="Type of source to load data from")
    file_type: Literal["csv", "json", "parquet","excel", "hl7", "ccda"] = Field(..., description="Type of file to load")
    connector: SFTPConnector | S3Connector | HTTPConnector | GCPConnector | AzureConnector | FTPConnector = Field(..., description="Configuration for the source connector")    