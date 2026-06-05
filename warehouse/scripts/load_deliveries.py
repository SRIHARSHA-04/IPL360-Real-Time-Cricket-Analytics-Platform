import pandas as pd
import psycopg2

df = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

cur = conn.cursor()

cur.execute("TRUNCATE TABLE fact_deliveries")

for _, row in df.iterrows():

    cur.execute(
        """
        INSERT INTO fact_deliveries(
            match_id,
            innings,
            batting_team,
            over_number,
            ball_number,
            batter,
            bowler,
            batter_runs,
            extras,
            total_runs,
            wicket
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            int(row["match_id"]),
            int(row["innings"]),
            row["batting_team"],
            int(row["over"]),
            int(row["ball"]),
            row["batter"],
            row["bowler"],
            int(row["batter_runs"]),
            int(row["extras"]),
            int(row["total_runs"]),
            int(row["wicket"])
        )
    )

conn.commit()

print(f"Loaded {len(df)} deliveries")

cur.close()
conn.close()