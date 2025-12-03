from sdk.core.connections.snowflake_client.snowflake_connection import SnowflakeConnection

def test_connection():
    sf_conn = SnowflakeConnection()
    try:
        conn = sf_conn.get_connection()
        cs = conn.cursor()
        cs.execute("SELECT CURRENT_VERSION()")
        version = cs.fetchone()[0]
        print(f"Connected to Snowflake version: {version}")
        cs.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Snowflake connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("Snowflake connection OK")
    else:
        print("Snowflake connection FAILED")
