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
    COUNT(*) AS balls,
    SUM(
        CASE
            WHEN batter_runs IN (4,6)
            THEN 1
            ELSE 0
        END
    ) AS boundaries,

    ROUND(
        (
            SUM(
                CASE
                    WHEN batter_runs IN (4,6)
                    THEN 1
                    ELSE 0
                END
            )::numeric * 100
        ) / COUNT(*),
        2
    ) AS boundary_percentage

FROM fact_deliveries

GROUP BY batter

HAVING COUNT(*) >= 500

ORDER BY boundary_percentage DESC

LIMIT 20;
"""

df = pd.read_sql(query, conn)

print("\n===== TOP BOUNDARY PERCENTAGE =====\n")
print(df)

conn.close()