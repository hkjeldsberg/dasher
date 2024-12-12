import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf

sns.set_theme()

np.random.seed(42)
# Setup
db_name = "src/db/dasher_stock.db"
table_name = "STOCKS"

# Create a connection to SQLite
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Drop table if exists
drop_table_query = f"""
DROP TABLE IF EXISTS {table_name}
"""
cursor.execute(drop_table_query)

# Create table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE NOT NULL,
    Open NUMERIC NOT NULL,
    Close NUMERIC NOT NULL,
    High NUMERIC NOT NULL,
    Low NUMERIC NOT NULL,
    Return NUMERIC NOT NULL,
    Volume INTEGER NOT NULL,
    Ticker TEXT NOT NULL
);
"""
cursor.execute(create_table_query)

days = [f"2024-12-{i:02d}" for i in range(31)]
days = np.linspace(0, 1, 10)
x = np.linspace(0, len(days), len(days))
tickers = [  # Oljefondet top 10
    "MSFT",  # Microsoft Corp
    "AAPL",  # Apple Inc
    "NVDA",  # NVIDIA Corp
    "GOOGL",  # Alphabet Inc
    "AMZN",  # Amazon.com Inc
    "META",  # Meta Platforms Inc
    "TSM",  # Taiwan Semiconductor Manufacturing Co Ltd
    "NVO",  # Novo Nordisk A/S
    "ASML",  # ASML Holding NV
    "LLY"  # Eli Lilly & Co
]
volumes = [
    453797,  # Microsoft Corp
    390805,  # Apple Inc
    377050,  # NVIDIA Corp
    258292,  # Alphabet Inc
    241291,  # Amazon.com Inc
    161219,  # Meta Platforms Inc
    148275,  # Taiwan Semiconductor Manufacturing Co Ltd
    120178,  # Novo Nordisk A/S
    111739,  # ASML Holding NV
    104040   # Eli Lilly & Co
]

start_date = "2020-01-01"
end_date = "2024-12-01"

dataframes = []
for i,ticker in enumerate(tickers):
    timeseries = yf.Ticker(ticker)
    history = timeseries.history(start=start_date, end=end_date, interval="1d")
    history = history[['Open', 'Close', 'High', 'Low', 'Volume']]
    history['Return'] = history['Close'].pct_change(1) * 100  # Return in percentage
    history['Ticker'] = ticker
    history['Volume'] = volumes[i]
    history.dropna(inplace=True)
    dataframes.append(history)

df = pd.concat(dataframes)

fig, ax = plt.subplots(1, 1)
for i, dep in enumerate(tickers):
    metric_name = "Return"
    metric = df.loc[df['Ticker'] == dep][metric_name]
    days = metric.index

    ax.plot(days, metric, label=dep)

plt.title("Stock data (Top 10 stocks NBIM)")
ax.legend()
plt.show()

df.to_sql(table_name, conn, if_exists='replace')

conn.commit()
conn.close()

print(f"Database '{db_name}' with table '{table_name}' created and populated with mock data.")
