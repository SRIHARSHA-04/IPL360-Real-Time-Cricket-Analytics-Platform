import pandas as pd

deliveries = pd.read_parquet(
    "data/curated/curated_deliveries.parquet"
)

# -------------------------
# Batting
# -------------------------

batting = (
    deliveries
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

# -------------------------
# Bowling
# -------------------------

bowling = (
    deliveries
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

# -------------------------
# Better fantasy formula
# -------------------------

players["fantasy_score"] = (
    players["runs"] * 0.08
    +
    players["strike_rate"] * 0.15
    +
    players["wickets"] * 1.2
)

players = players.sort_values(
    "fantasy_score",
    ascending=False
)

players.to_csv(
    "ml/fantasy/player_rankings.csv",
    index=False
)

print("\n===== PLAYER RANKINGS CREATED =====\n")

print(
    players[
        [
            "batter",
            "runs",
            "strike_rate",
            "wickets",
            "fantasy_score"
        ]
    ].head(25)
)