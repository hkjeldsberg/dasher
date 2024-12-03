import sqlite3

import pandas as pd
from matplotlib import pyplot as plt

from src.config import DATABASE_URL, TABLE_NAME


def fetch_data(plain_sql=False):
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
    df['datetime'] = pd.to_datetime(df['report_date'], format='%Y-%m-%d')
    df['date'] = pd.to_datetime(df['report_date'], format='%Y-%m-%d')
    df.set_index('date', inplace=True)
    return df


def plot_data(df):
    print(df.head())

    df.groupby("department").risk_score.plot()
    plt.legend()
    plt.show()
