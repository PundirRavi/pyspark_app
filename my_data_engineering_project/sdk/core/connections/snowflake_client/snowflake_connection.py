from snowflake.connector import connect
from sdk.configs.settings import settings

class SnowflakeConnection:
    def __init__(self):
        self.user = settings.snowflake.user
        self.password = settings.snowflake.password
        self.account = settings.snowflake.account
        self.warehouse = getattr(settings.snowflake, "warehouse", None)  # Use getattr to allow missing
        self.database = settings.snowflake.database
        self.schema = settings.snowflake.schema
        self.role = getattr(settings.snowflake, "role", None) # optional

    def get_connection(self, database: str = None, schema: str = None):
        conn_params = {
            "user": self.user,
            "password": self.password,
            "account": self.account,
            "database": database or self.database,
            "schema": schema or self.schema,
        }
        if self.warehouse:
            conn_params["warehouse"] = self.warehouse
        if self.role:
            conn_params["role"] = self.role

        return connect(**conn_params)
    

    def list_databases_and_schemas(self):
        ctx = self.get_connection()   # Get connection using existing method
        cs = ctx.cursor()
        try:
            cs.execute("SHOW DATABASES")
            databases = [row[1] for row in cs.fetchall()]
            db_schemas = {}
            for db in databases:
                cs.execute(f"SHOW SCHEMAS IN DATABASE {db}")
                schemas = [row[1] for row in cs.fetchall()]
                db_schemas[db] = schemas
            return db_schemas
        finally:
            cs.close()
            ctx.close()


    def get_liquibase_connection_params(self, database: str = None, schema: str = None):
        return {
            "url": f"jdbc:snowflake://{self.account}.snowflakecomputing.com/?db={database or self.database}&schema={schema or self.schema}",
            "driver": "net.snowflake.client.jdbc.SnowflakeDriver",
            "username": self.user,
            "password": self.password,
            "account": self.account
        }
