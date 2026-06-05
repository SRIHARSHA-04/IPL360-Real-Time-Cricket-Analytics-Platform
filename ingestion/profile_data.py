import pandas as pd

matches = pd.read_csv("data/raw/matches.csv")
deliveries = pd.read_csv("data/raw/deliveries.csv")

print("\n===== DATA PROFILE =====\n")

print("Total Matches:", len(matches))

print("Total Deliveries:", len(deliveries))

print("\nTop Venues:")

print(
    matches["venue"]
    .value_counts()
    .head(10)
)

print("\nTop Teams:")

teams = pd.concat([
    matches["team1"],
    matches["team2"]
])

print(
    teams.value_counts()
    .head(10)
)

print("\nTop Run Scorers:")

print(
    deliveries.groupby("batter")["runs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)