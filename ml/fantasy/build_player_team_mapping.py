import pandas as pd

deliveries = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

player_team = (
    deliveries[
        ["batter", "batting_team"]
    ]
    .drop_duplicates()
)

player_team.columns = [
    "player",
    "team"
]

player_team.to_csv(
    "ml/fantasy/player_team_mapping.csv",
    index=False
)

print(
    "\n===== PLAYER TEAM MAPPING CREATED =====\n"
)

print(player_team.head(20))

print(
    "\nPlayers:",
    len(player_team)
)