import json
import streamlit as st
import joblib
import pandas as pd

from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Live Match Center",
    layout="wide"
)

st.title("🏏 IPL360 Live Match Center")

st_autorefresh(
    interval=500,
    key="live_refresh"
)

try:

    with open(
        "dashboard/live/live_match_state.json",
        "r"
    ) as f:

        state = json.load(f)

except:

    st.warning(
        "Waiting for live match data..."
    )
    st.stop()

predicted_score = None

try:

    model = joblib.load(
        "models/score_predictor.pkl"
    )

    if (
        state["innings"] == 1
        and state["overs_float"] > 0
    ):

        run_rate = (
            state["score"]
            / state["overs_float"]
        )

        features = pd.DataFrame(
            [{
                "current_score":
                state["score"],

                "wickets":
                state["wickets"],

                "overs":
                state["overs_float"],

                "run_rate":
                run_rate
            }]
        )

        predicted_score = round(
            model.predict(features)[0]
        )

except:
    pass

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Innings",
    state["innings"]
)

c2.metric(
    "Score",
    f"{state['score']}/{state['wickets']}"
)

c3.metric(
    "Wickets",
    state["wickets"]
)

c4.metric(
    "Overs",
    state["display_over"]
)

c5.metric(
    "Predicted Score",
    predicted_score
    if predicted_score
    else "-"
)

st.divider()

st.subheader(
    "Current Delivery"
)

st.write(
    f"Over: {state['display_over']}"
)

st.write(
    f"Batter: {state['batter']}"
)

st.write(
    f"Bowler: {state['bowler']}"
)

st.write(
    f"Runs: {state['runs']}"
)

if state["innings"] == 2:

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Target",
        state.get(
            "target",
            "-"
        )
    )

    c2.metric(
        "Runs Needed",
        state.get(
            "runs_needed",
            "-"
        )
    )

    c3.metric(
        "Balls Remaining",
        state.get(
            "balls_remaining",
            "-"
        )
    )

    c4.metric(
        "Win Probability",
        f"{state.get('win_probability',0)}%"
    )