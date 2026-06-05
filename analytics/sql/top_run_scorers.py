import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
SELECT
    batter,
    SUM(batter_runs) AS total_runs
FROM fact_deliveries
GROUP BY batter
ORDER BY total_runs DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()