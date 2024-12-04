import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import splev, splrep

sns.set_theme()

np.random.seed(42)
# Setup
db_name = "src/db/dasher.db"
table_name = "reports"

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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE NOT NULL,
    department TEXT NOT NULL,
    risk_score REAL NOT NULL,
    financial_metric REAL NOT NULL
);
"""
cursor.execute(create_table_query)

days = [f"2024-12-{i:02d}" for i in range(31)]
x = np.linspace(0, len(days), len(days))
deps = ["FinTech", "Backend", "Frontend", "DevOps", "MLOps", "PropTech", "FullStack", "DataEng", "DataSci"]

vals = np.linspace(np.exp(1), 10, len(days))
mock_data = []


def get_metric(x, dep_n):
    return 10000 * (0.15 * dep_n + x * np.log(x) ** (np.random.randn() * 0.5))


def get_risk(x, dep_n):
    return np.abs(10 + dep_n + 2 * x * np.log(x) * (-np.random.randn() * 0.25))


def map_int_to_date(start_date, days):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    result_date = start + timedelta(days=days)
    return result_date.strftime("%Y-%m-%d")


start_date = "2024-01-01"
n_days = 366
dt = np.pi / int(n_days / 2)
days_new = np.arange(0, 2 * np.pi, dt)
days_int = np.linspace(0, len(days_new), len(days_new))

fig, ax = plt.subplots(1, 2)
for i, dep in enumerate(deps):
    v = []
    r = []
    for j, day in enumerate(days):
        metric = get_metric(vals[j], i)
        risk_score = get_risk(vals[j], i)
        v.append(metric)
        r.append(risk_score)

    tck_v = splrep(x, v, s=1e-15, k=3)
    tck_r = splrep(x, r, s=1, k=3)

    vnew = splev(days_new, tck_v)
    rnew = splev(days_new, tck_r)

    ax[0].plot(days_new, vnew, "o-", label=f"metric (dep={dep})")
    ax[1].plot(days_new, rnew, "o-", label=f"risk (dep={dep})")

    for met, risk, day in zip(vnew, rnew, days_int):
        mapped_date = map_int_to_date(start_date, day)

        data = (mapped_date, dep, risk, met)
        mock_data.append(data)

plt.title("Generated mock data")
ax[0].legend()
ax[1].legend()
plt.show()

# Insert mock data
insert_query = f"""
INSERT INTO {table_name} (report_date, department, risk_score, financial_metric)
VALUES (?, ?, ?, ?);
"""
cursor.executemany(insert_query, mock_data)

conn.commit()
conn.close()

print(f"Database '{db_name}' with table '{table_name}' created and populated with mock data.")
