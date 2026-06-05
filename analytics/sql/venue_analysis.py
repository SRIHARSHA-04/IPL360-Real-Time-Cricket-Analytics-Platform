import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
SELECT
    venue,
    COUNT(*) AS matches
FROM dim_matches
GROUP BY venue
ORDER BY matches DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()