import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
SELECT
    winner,
    COUNT(*) AS wins
FROM dim_matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY wins DESC;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()
