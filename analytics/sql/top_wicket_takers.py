import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
SELECT
    bowler,
    SUM(wicket) AS wickets
FROM fact_deliveries
GROUP BY bowler
ORDER BY wickets DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()