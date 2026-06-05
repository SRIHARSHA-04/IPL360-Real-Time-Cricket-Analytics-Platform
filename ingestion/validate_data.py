import pandas as pd

matches = pd.read_csv("data/raw/matches.csv")
deliveries = pd.read_csv("data/raw/deliveries.csv")
players = pd.read_csv("data/raw/players.csv")

print("\n========== DATA VALIDATION ==========\n")

print("Matches Shape:", matches.shape)
print("Deliveries Shape:", deliveries.shape)
print("Players Shape:", players.shape)

print("\n--- Missing Values ---")
print(matches.isnull().sum())

print("\n--- Duplicate Match IDs ---")
print(matches["match_id"].duplicated().sum())

print("\n--- Unique Teams ---")
teams = pd.concat([
    matches["team1"],
    matches["team2"]
]).dropna().unique()

print(len(teams))

print("\n--- Unique Players ---")
print(players["player_name"].nunique())

print("\n--- Deliveries with Missing Batter ---")
print(deliveries["batter"].isnull().sum())

print("\n--- Deliveries with Missing Bowler ---")
print(deliveries["bowler"].isnull().sum())

print("\nValidation Complete")