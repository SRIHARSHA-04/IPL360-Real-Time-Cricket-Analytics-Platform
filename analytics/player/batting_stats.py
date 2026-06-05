import pandas as pd
from pathlib import Path

CURATED_DIR = Path("data/curated")
ANALYTICS_DIR = Path("data/analytics")

ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(
    CURATED_DIR / "curated_deliveries.parquet"
)

# Runs
runs_df = (
    df.groupby("batter")["batter_runs"]
    .sum()
    .reset_index(name="runs")
)

# Balls faced
balls_df = (
    df.groupby("batter")
    .size()
    .reset_index(name="balls_faced")
)

# Matches played
matches_df = (
    df.groupby("batter")["match_id"]
    .nunique()
    .reset_index(name="matches")
)

# Fours
fours_df = (
    df[df["batter_runs"] == 4]
    .groupby("batter")
    .size()
    .reset_index(name="fours")
)

# Sixes
sixes_df = (
    df[df["batter_runs"] == 6]
    .groupby("batter")
    .size()
    .reset_index(name="sixes")
)

# Merge everything
batting_stats = runs_df.merge(
    balls_df,
    on="batter"
)

batting_stats = batting_stats.merge(
    matches_df,
    on="batter"
)

batting_stats = batting_stats.merge(
    fours_df,
    on="batter",
    how="left"
)

batting_stats = batting_stats.merge(
    sixes_df,
    on="batter",
    how="left"
)

batting_stats["fours"] = batting_stats["fours"].fillna(0)
batting_stats["sixes"] = batting_stats["sixes"].fillna(0)

# Strike Rate
batting_stats["strike_rate"] = (
    batting_stats["runs"]
    / batting_stats["balls_faced"]
) * 100

# Sort
batting_stats = batting_stats.sort_values(
    "runs",
    ascending=False
)

# Save
batting_stats.to_parquet(
    ANALYTICS_DIR / "player_batting_stats.parquet",
    index=False
)

print("\n===== TOP 20 RUN SCORERS =====\n")

print(
    batting_stats[
        [
            "batter",
            "runs",
            "balls_faced",
            "strike_rate",
            "matches",
            "fours",
            "sixes"
        ]
    ].head(20)
)