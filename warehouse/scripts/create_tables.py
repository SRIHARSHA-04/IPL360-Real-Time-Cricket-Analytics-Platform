import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="ipl360",
    user="sriharsha"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS dim_matches(
    match_id BIGINT PRIMARY KEY,
    match_date DATE,
    venue TEXT,
    team1 TEXT,
    team2 TEXT,
    winner TEXT,
    season TEXT,
    city TEXT,
    match_type TEXT,
    toss_winner TEXT,
    toss_decision TEXT,
    player_of_match TEXT
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS fact_deliveries(
    delivery_id BIGSERIAL PRIMARY KEY,
    match_id BIGINT,
    innings INTEGER,
    batting_team TEXT,
    over_number INTEGER,
    ball_number INTEGER,
    batter TEXT,
    bowler TEXT,
    batter_runs INTEGER,
    extras INTEGER,
    total_runs INTEGER,
    wicket INTEGER
);
""")

conn.commit()

print("Warehouse tables created")

cur.close()
conn.close()