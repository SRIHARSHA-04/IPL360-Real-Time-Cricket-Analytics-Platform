import pandas as pd

squads = pd.read_csv(
    "ml/fantasy/current_squads.csv"
)

available_teams = sorted(
    squads["team"].unique()
)

print("\nAvailable Teams:\n")

for team in available_teams:
    print(team)

print()

TEAM1 = input(
    "\nEnter Team 1: "
)

TEAM2 = input(
    "Enter Team 2: "
)

rankings = pd.read_csv(
    "ml/fantasy/current_player_rankings.csv"
)

squads = pd.read_csv(
    "ml/fantasy/current_squads.csv"
)

metadata = pd.read_csv(
    "ml/fantasy/player_metadata.csv"
)

pool = squads[
    (
        squads["team"] == TEAM1
    )
    |
    (
        squads["team"] == TEAM2
    )
]

fantasy_pool = rankings.merge(
    pool,
    left_on="batter",
    right_on="player",
    how="inner"
)

fantasy_pool = fantasy_pool.merge(
    metadata,
    left_on="batter",
    right_on="player",
    how="left"
)

fantasy_pool = fantasy_pool.sort_values(
    "fantasy_score",
    ascending=False
)

selected = []

# ---------------------
# 1 WK
# ---------------------

wk = fantasy_pool[
    fantasy_pool["role"] == "WK"
].head(1)

selected.extend(
    wk["batter"].tolist()
)

# ---------------------
# 3 BAT
# ---------------------

bat = fantasy_pool[
    (fantasy_pool["role"] == "BAT")
    &
    (~fantasy_pool["batter"].isin(selected))
].head(3)

selected.extend(
    bat["batter"].tolist()
)

# ---------------------
# 2 AR
# ---------------------

ar = fantasy_pool[
    (fantasy_pool["role"] == "AR")
    &
    (~fantasy_pool["batter"].isin(selected))
].head(2)

selected.extend(
    ar["batter"].tolist()
)

# ---------------------
# 3 BOWL
# ---------------------

bowl = fantasy_pool[
    (fantasy_pool["role"] == "BOWL")
    &
    (~fantasy_pool["batter"].isin(selected))
].head(3)

selected.extend(
    bowl["batter"].tolist()
)

# ---------------------
# Fill remaining slots
# ---------------------

remaining = fantasy_pool[
    ~fantasy_pool["batter"].isin(
        selected
    )
]

selected.extend(
    remaining.head(
        11 - len(selected)
    )["batter"].tolist()
)

final_team = fantasy_pool[
    fantasy_pool["batter"].isin(
        selected
    )
]

final_team = final_team.sort_values(
    "fantasy_score",
    ascending=False
)

print(
    f"\n===== {TEAM1} vs {TEAM2} =====\n"
)

print(
    "===== FANTASY XI =====\n"
)

for i, row in enumerate(
    final_team.itertuples(),
    start=1
):

    tag = ""

    if i == 1:
        tag = " (C)"

    elif i == 2:
        tag = " (VC)"

    print(
        f"{i}. "
        f"{row.batter}"
        f"{tag}"
        f" | {row.role}"
        f" | {row.team}"
        f" | Score {row.fantasy_score:.2f}"
    )

print("\nTeam Composition")

print(
    final_team["role"]
    .value_counts()
)