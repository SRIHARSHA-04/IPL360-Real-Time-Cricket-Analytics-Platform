import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
WITH player_stats AS (

    SELECT
        batter,

        SUM(batter_runs) AS runs,

        COUNT(*) AS balls,

        SUM(wicket) AS dismissals,

        ROUND(
            SUM(batter_runs)::numeric /
            NULLIF(SUM(wicket),0),
            2
        ) AS average,

        ROUND(
            (SUM(batter_runs)::numeric * 100) /
            COUNT(*),
            2
        ) AS strike_rate,

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
        ) AS boundary_pct

    FROM fact_deliveries

    GROUP BY batter

    HAVING SUM(batter_runs) >= 1000
)

SELECT
    batter,
    runs,
    average,
    strike_rate,
    boundary_pct,

    ROUND(
        (
            average * 0.30 +
            strike_rate * 0.30 +
            boundary_pct * 0.20 +
            runs / 100 * 0.20
        ),
        2
    ) AS impact_score

FROM player_stats

ORDER BY impact_score DESC

LIMIT 20;
"""

df = pd.read_sql(query, conn)

print("\n===== PLAYER IMPACT SCORE =====\n")
print(df)

conn.close()