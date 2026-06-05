import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
SELECT
    batter,
    SUM(batter_runs) AS runs,
    COUNT(*) AS balls,
    ROUND(
        (SUM(batter_runs)::numeric * 100) /
        COUNT(*),
        2
    ) AS strike_rate
FROM fact_deliveries
GROUP BY batter
HAVING SUM(batter_runs) >= 1000
ORDER BY strike_rate DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)

print("\n===== TOP STRIKE RATES =====\n")
print(df)

conn.close()