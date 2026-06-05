import streamlit as st
import pandas as pd

st.title("🎯 Fantasy XI Generator")

rankings = pd.read_csv(
    "ml/fantasy/current_player_rankings.csv"
)

squads = pd.read_csv(
    "ml/fantasy/current_squads.csv"
)

metadata = pd.read_csv(
    "ml/fantasy/player_metadata.csv"
)

teams = sorted(
    squads["team"].unique()
)

team1 = st.selectbox(
    "Team 1",
    teams
)

team2 = st.selectbox(
    "Team 2",
    teams,
    index=1
)

if st.button("Generate Fantasy XI"):

    pool = squads[
        (
            squads["team"] == team1
        )
        |
        (
            squads["team"] == team2
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

    wk = fantasy_pool[
        fantasy_pool["role"] == "WK"
    ].head(1)

    selected.extend(
        wk["batter"].tolist()
    )

    bat = fantasy_pool[
        (
            fantasy_pool["role"] == "BAT"
        )
        &
        (
            ~fantasy_pool["batter"].isin(
                selected
            )
        )
    ].head(3)

    selected.extend(
        bat["batter"].tolist()
    )

    ar = fantasy_pool[
        (
            fantasy_pool["role"] == "AR"
        )
        &
        (
            ~fantasy_pool["batter"].isin(
                selected
            )
        )
    ].head(2)

    selected.extend(
        ar["batter"].tolist()
    )

    bowl = fantasy_pool[
        (
            fantasy_pool["role"] == "BOWL"
        )
        &
        (
            ~fantasy_pool["batter"].isin(
                selected
            )
        )
    ].head(3)

    selected.extend(
        bowl["batter"].tolist()
    )

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

    st.subheader(
        f"{team1} vs {team2}"
    )

    captain = final_team.iloc[0]["batter"]
    vice_captain = final_team.iloc[1]["batter"]

    st.success(
        f"Captain: {captain}"
    )

    st.info(
        f"Vice Captain: {vice_captain}"
    )

    st.dataframe(
        final_team[
            [
                "batter",
                "team",
                "role",
                "fantasy_score"
            ]
        ]
    )

    st.subheader(
        "Team Composition"
    )

    st.dataframe(
        final_team["role"]
        .value_counts()
        .reset_index()
    )