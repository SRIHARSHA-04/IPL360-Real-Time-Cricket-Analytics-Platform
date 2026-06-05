import pandas as pd

players = pd.read_csv(
    "ml/fantasy/player_rankings.csv"
)

top11 = players.head(11)

print("\n===== FANTASY XI =====\n")

for i, row in enumerate(
    top11.itertuples(),
    start=1
):
    print(
        f"{i}. {row.batter} "
        f"(Score: {row.fantasy_score:.2f})"
    )

print("\nCaptain:")
print(top11.iloc[0]["batter"])

print("\nVice Captain:")
print(top11.iloc[1]["batter"])