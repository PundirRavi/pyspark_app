import subprocess
import os
from sdk.core.utils.logger import logger

def deploy_schema(db_type: str, database: str, schema: str, schema_version: str, connection_params: dict):
    """
    Deploy schema using Liquibase CLI.
    connection_params: dict with keys: url, driver, username, password
    """
    # Compose changelog path dynamically 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    liquibase_folder = os.path.abspath(os.path.join(base_dir, "../liquibase"))
    # Append insecureMode=true if not already present
    jdbc_url = connection_params['url']
    if "insecureMode=true" not in jdbc_url:
        separator = "&" if "?" in jdbc_url else "?"
        jdbc_url = jdbc_url + f"{separator}insecureMode=true"

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{liquibase_folder}:/changelogs",
        "my-liquibase-image",
        f"--url={jdbc_url}",
        "--username", connection_params["username"],
        "--password", connection_params["password"],
        "--changeLogFile=/changelogs/db.changelog-master.xml",
        "update"
        ]

    logger.info(f"Executing Liquibase command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"Liquibase output: {result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Liquibase error: {e.stderr}")
        return False, e.stderr
