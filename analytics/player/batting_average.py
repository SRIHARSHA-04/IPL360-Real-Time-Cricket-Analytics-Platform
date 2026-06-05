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
    SUM(wicket) AS dismissals,
    ROUND(
        SUM(batter_runs)::numeric /
        NULLIF(SUM(wicket), 0),
        2
    ) AS batting_average
FROM fact_deliveries
GROUP BY batter
HAVING SUM(batter_runs) >= 1000
ORDER BY batting_average DESC
LIMIT 20;
"""

df = pd.read_sql(query, conn)

print("\n===== TOP BATTING AVERAGES =====\n")
print(df)

conn.close()