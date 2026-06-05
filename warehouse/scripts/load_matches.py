import pandas as pd
import psycopg2

df = pd.read_parquet(
    "data/curated/curated_matches.parquet"
)

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

cur = conn.cursor()

cur.execute("TRUNCATE TABLE dim_matches")

for _, row in df.iterrows():

    cur.execute(
        """
        INSERT INTO dim_matches(
            match_id,
            match_date,
            venue,
            team1,
            team2,
            winner,
            season,
            city,
            match_type,
            toss_winner,
            toss_decision,
            player_of_match
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            int(row["match_id"]),
            row["date"],
            row["venue"],
            row["team1"],
            row["team2"],
            row["winner"],
            row["season"],
            row["city"],
            row["match_type"],
            row["toss_winner"],
            row["toss_decision"],
            row["player_of_match"]
        )
    )

conn.commit()

print(f"Loaded {len(df)} matches")

cur.close()
conn.close()