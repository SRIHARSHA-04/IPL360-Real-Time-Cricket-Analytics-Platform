import pandas as pd

matches = pd.read_parquet(
    "data/curated/curated_matches.parquet"
)

deliveries = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

# Fix datatype mismatch
matches["match_id"] = (
    matches["match_id"]
    .astype(str)
)

deliveries["match_id"] = (
    deliveries["match_id"]
    .astype(str)
)

latest_season = (
    matches["season"]
    .astype(str)
    .max()
)

season_matches = matches[
    matches["season"]
    .astype(str)
    == latest_season
]

match_ids = set(
    season_matches["match_id"]
)

season_deliveries = deliveries[
    deliveries["match_id"]
    .isin(match_ids)
]

print(
    f"\nLatest Season: {latest_season}"
)

print(
    f"Season Matches: {len(season_matches)}"
)

print(
    f"Season Deliveries: {len(season_deliveries)}"
)

squads = (
    season_deliveries[
        [
            "batting_team",
            "batter"
        ]
    ]
    .drop_duplicates()
)

squads.columns = [
    "team",
    "player"
]

squads = squads.sort_values(
    ["team", "player"]
)

squads.to_csv(
    "ml/fantasy/current_squads.csv",
    index=False
)

print(
    f"\nPlayers Found: {len(squads)}"
)

print()
print(squads.head(20))