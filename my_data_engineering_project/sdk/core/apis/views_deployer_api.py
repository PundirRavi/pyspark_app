# deploy_views.py

import os
import sys
import glob
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from google.cloud import bigquery
from sdk.configs.settings import settings
from sdk.core.utils.logger import logger
from sdk.google_client.gcp_client import get_gcp_client

logger.info("Initializing views deployer...")
# deploy_views.py
# This script deploys SQL views to Google BigQuery and tracks metadata in a BigQuery table.
# Ensure the environment is set up correctly
# with the necessary GCP credentials and BigQuery dataset.
logger.info("Loading GCP settings...")

DATASET_ID = settings.gcp.meta_dataset
TABLE_ID = "view_deployments"

bq_client = get_gcp_client()

print(f"created bq_client: {bq_client}")



# --- 1. Create metadata table if not exists ---
def create_metadata_table():
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    schema = [
        bigquery.SchemaField("view_name", "STRING"),
        bigquery.SchemaField("version", "STRING"),
        bigquery.SchemaField("deployed_by", "STRING"),
        bigquery.SchemaField("deployed_at", "TIMESTAMP"),
        bigquery.SchemaField("file_path", "STRING"),
        bigquery.SchemaField("comment", "STRING"),
    ]
    table = bigquery.Table(table_ref, schema=schema)
    try:
        bq_client.get_table(table)
        print("Metadata table exists.")
    except Exception:
        bq_client.create_table(table)
        print("Created metadata table.")

# --- 2. Deploy SQL View File ---
def deploy_view(sql_path: str):
    with open(sql_path, 'r') as file:
        content = file.read()

    # Extract view name and version from filename
    filename = os.path.basename(sql_path)
    view_name = filename.split(".")[0].rsplit("_v", 1)[0]
    version = "v" + filename.split("_v")[-1].split(".")[0]

    query = content.replace("{{project_id}}", PROJECT_ID)

    print(f"Deploying {view_name} ({version})...")
    bq_client.query(query).result()

    row = [
        {
            "view_name": view_name,
            "version": version,
            "deployed_by": os.getenv("USER", "ci_cd"),
            "deployed_at": datetime.datetime.utcnow(),
            "file_path": sql_path,
            "comment": "Auto deployed via script"
        }
    ]

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    errors = bq_client.insert_rows_json(table_ref, row)
    if errors:
        print(f"❌ Error inserting metadata: {errors}")
    else:
        print(f"✅ Deployed and tracked: {view_name} ({version})")

# --- 3. Deploy all .sql files from views folder ---
def deploy_all_views():
    sql_paths = glob.glob("sql/views/**/*.sql", recursive=True)
    for path in sql_paths:
        deploy_view(path)

if __name__ == "__main__":
    create_metadata_table()
    #deploy_all_views()
