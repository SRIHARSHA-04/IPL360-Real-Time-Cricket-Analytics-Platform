import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

matches = pd.read_csv(RAW_DIR / "matches.csv")
deliveries = pd.read_csv(RAW_DIR / "deliveries.csv")
players = pd.read_csv(RAW_DIR / "players.csv")

TEAM_MAPPING = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
}

for col in ["team1", "team2", "winner"]:
    matches[col] = matches[col].replace(TEAM_MAPPING)

deliveries["batting_team"] = deliveries["batting_team"].replace(
    TEAM_MAPPING
)

matches.to_parquet(
    PROCESSED_DIR / "processed_matches.parquet",
    index=False
)

deliveries.to_parquet(
    PROCESSED_DIR / "processed_deliveries.parquet",
    index=False
)

players.to_parquet(
    PROCESSED_DIR / "processed_players.parquet",
    index=False
)

print("Processed layer created successfully")
print("Matches:", len(matches))
print("Deliveries:", len(deliveries))
print("Players:", len(players))
