import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

query = """
WITH team_matches AS (

    SELECT team1 AS team
    FROM dim_matches

    UNION ALL

    SELECT team2 AS team
    FROM dim_matches

),

matches_played AS (

    SELECT
        team,
        COUNT(*) AS matches
    FROM team_matches
    GROUP BY team

),

wins AS (

    SELECT
        winner AS team,
        COUNT(*) AS wins
    FROM dim_matches
    WHERE winner <> 'NaN'
    GROUP BY winner

)

SELECT
    m.team,
    m.matches,
    COALESCE(w.wins,0) AS wins,

    ROUND(
        (
            COALESCE(w.wins,0)::numeric
            * 100
        ) / m.matches,
        2
    ) AS win_percentage

FROM matches_played m

LEFT JOIN wins w
ON m.team = w.team

ORDER BY win_percentage DESC;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()