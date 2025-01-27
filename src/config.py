from starlette.config import Config

config = Config(".env")

SNOWFLAKE_USER = "hak47"
SNOWFLAKE_PASSWORD = config("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = "ac15843.north-europe.azure"
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "DASHER"
SNOWFLAKE_SCHEMA = "FILES"
SNOWFLAKE_TABLE_NAME = ""

DATABASE_URL = "/Users/hkjeldsberg/Projects/dasher/src/db/dasher_stock.db"
TABLE_NAME = "STOCKS"
