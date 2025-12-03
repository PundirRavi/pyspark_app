from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import os
from sdk.core.connections.snowflake_client.snowflake_connection import SnowflakeConnection
from sdk.core.liquibase.deploy import deploy_schema
from sdk.core.utils.logger import logger
from sdk.configs.schema_config import SCHEMA_CONFIG

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../../templates"))

@router.get("/deploy-schema")
async def get_deploy_page(request: Request, db_type: str = None):
    config = SCHEMA_CONFIG

    # Only list database types statically
    database_types = list(config.keys())

    # For Snowflake, fetch dynamic DBs and schemas, else empty lists
    if db_type and db_type.lower() == "snowflake":
        sf_conn = SnowflakeConnection()
        db_schemas = sf_conn.list_databases_and_schemas()
        databases = list(db_schemas.keys())
        schemas = db_schemas.get(databases[0], []) if databases else []
    else:
        databases = []
        schemas = []

    schema_versions = config.get(db_type, {}).get("schema_versions", []) if db_type else []

    return templates.TemplateResponse("deploy_schema.html", {
        "request": request,
        "database_types": database_types,
        "selected_dbtype": db_type,
        "databases": databases,
        "schemas": schemas,
        "schema_versions": schema_versions,
        "message": None
    })

@router.get("/api/schemas")
async def get_schemas(db: str):
    if not db:
        return JSONResponse(content={"schemas": []})
    sf_conn = SnowflakeConnection()
    try:
        schemas = sf_conn.list_databases_and_schemas().get(db, [])
    except Exception:
        schemas = []
    return JSONResponse(content={"schemas": schemas})

@router.post("/deploy-schema")
async def submit_deploy_schema(request: Request,
                               db_type: str = Form(...),
                               database: str = Form(...),
                               schema: str = Form(...),
                               schema_version: str = Form(...)):
    logger.info(f"Deploy requested: db_type={db_type}, database={database}, schema={schema}, schema_version={schema_version}")

    try:
        if db_type.lower() == "snowflake":
            sf_conn = SnowflakeConnection()
            conn_params = sf_conn.get_liquibase_connection_params(database, schema)
            success, output = deploy_schema(db_type, database, schema, schema_version, conn_params)
        else:
            raise NotImplementedError(f"Deploy not implemented for db_type {db_type}")

        message = f"Successfully deployed schema version {schema_version}." if success else f"Deployment failed: {output}"
        if success:
            logger.info(message)
        else:
            logger.error(message)
    except Exception as e:
        message = f"Error during deployment: {e}"
        logger.error(message)

    # Reload database types only, other lists cleared to refresh dynamically next time
    database_types = list(SCHEMA_CONFIG.keys())

    return templates.TemplateResponse("deploy_schema.html", {
        "request": request,
        "database_types": database_types,
        "selected_dbtype": db_type,
        "databases": [],
        "schemas": [],
        "schema_versions": SCHEMA_CONFIG.get(db_type, {}).get("schema_versions", []),
        "message": message
    })
