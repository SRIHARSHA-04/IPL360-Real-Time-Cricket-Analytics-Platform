import pandas as pd
from pathlib import Path

CURATED_DIR = Path("data/curated")
OUTPUT_DIR = Path("ml/features")

deliveries = pd.read_parquet(
    CURATED_DIR / "curated_deliveries.parquet"
)

features = []

for match_id in deliveries["match_id"].unique():

    match_df = deliveries[
        deliveries["match_id"] == match_id
    ]

    innings1 = match_df[
        match_df["innings"] == 1
    ].copy()

    if len(innings1) == 0:
        continue

    final_score = innings1["total_runs"].sum()

    innings1["cumulative_runs"] = (
        innings1["total_runs"].cumsum()
    )

    innings1["cumulative_wickets"] = (
        innings1["wicket"].cumsum()
    )

    innings1["balls_bowled"] = range(
        1,
        len(innings1) + 1
    )

    for _, row in innings1.iterrows():

        balls = row["balls_bowled"]

        overs = balls / 6

        if overs == 0:
            continue

        run_rate = (
            row["cumulative_runs"] / overs
        )

        features.append(
            {
                "match_id": match_id,
                "current_score": row["cumulative_runs"],
                "wickets": row["cumulative_wickets"],
                "overs": round(overs, 2),
                "run_rate": round(run_rate, 2),
                "final_score": final_score
            }
        )

features_df = pd.DataFrame(features)

features_df.to_csv(
    OUTPUT_DIR / "score_prediction_features.csv",
    index=False
)

print("\n===== FEATURES CREATED =====")
print(features_df.head())
print()
print("Rows:", len(features_df))