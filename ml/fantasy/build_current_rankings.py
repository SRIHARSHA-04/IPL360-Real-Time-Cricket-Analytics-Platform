import pandas as pd

matches = pd.read_parquet(
    "data/curated/curated_matches.parquet"
)

deliveries = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

matches["match_id"] = matches["match_id"].astype(str)
deliveries["match_id"] = deliveries["match_id"].astype(str)

latest_season = (
    matches["season"]
    .astype(str)
    .max()
)

season_matches = matches[
    matches["season"] == latest_season
]

match_ids = set(
    season_matches["match_id"]
)

season_deliveries = deliveries[
    deliveries["match_id"]
    .isin(match_ids)
]

batting = (
    season_deliveries
    .groupby("batter")
    .agg(
        runs=("batter_runs", "sum"),
        balls=("batter_runs", "count")
    )
    .reset_index()
)

batting["strike_rate"] = (
    batting["runs"]
    /
    batting["balls"]
) * 100

bowling = (
    season_deliveries
    .groupby("bowler")
    .agg(
        wickets=("wicket", "sum")
    )
    .reset_index()
)

players = batting.merge(
    bowling,
    left_on="batter",
    right_on="bowler",
    how="outer"
)

players["runs"] = players["runs"].fillna(0)
players["balls"] = players["balls"].fillna(0)
players["strike_rate"] = players["strike_rate"].fillna(0)
players["wickets"] = players["wickets"].fillna(0)

players["fantasy_score"] = (
    players["runs"] * 0.25
    +
    players["strike_rate"] * 0.15
    +
    players["wickets"] * 8
)

players.to_csv(
    "ml/fantasy/current_player_rankings.csv",
    index=False
)

players = players.sort_values(
    "fantasy_score",
    ascending=False
)

print("\n===== 2026 PLAYER RANKINGS =====\n")

print(
    players[
        [
            "batter",
            "runs",
            "strike_rate",
            "wickets",
            "fantasy_score"
        ]
    ].head(20)
)