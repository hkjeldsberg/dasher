import sqlite3

import pandas as pd
import snowflake.connector
from matplotlib import pyplot as plt

from src.config import (
    DATABASE_URL,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE,
    TABLE_NAME,
)


def fetch_data_from_snowflake():
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

    query = f"SELECT * FROM {TABLE_NAME};"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=col_names)
    conn.close()

    return df


def fetch_data_from_sqlite(plain_sql=False):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    query = f"SELECT * FROM {TABLE_NAME};"
    if plain_sql:
        cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            print(row)

        return rows
    else:
        df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def prepare_data(df):
    df.columns = map(lambda x: str(x).upper(), df.columns)
    df["DATETIME"] = pd.to_datetime(df["REPORT_DATE"], format="%Y-%m-%d")
    df["DATE"] = pd.to_datetime(df["REPORT_DATE"], format="%Y-%m-%d")
    df.set_index("DATE", inplace=True)

    return df


def plot_data(df):
    df.groupby("DEPARTMENT").risk_score.plot()
    plt.legend()
    plt.show()
