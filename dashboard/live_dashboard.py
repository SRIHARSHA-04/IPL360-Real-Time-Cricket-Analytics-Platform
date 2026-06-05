import json
import streamlit as st
import joblib
import pandas as pd

from streamlit_autorefresh import st_autorefresh

st_autorefresh(
    interval=500,
    key="live_refresh"
)

st.set_page_config(
    page_title="IPL360 Live Match Center",
    layout="wide"
)

SCORE_MODEL = joblib.load(
    "models/score_predictor.pkl"
)

st.title(
    "🏏 IPL360 Live Match Center"
)

try:

    with open(
        "dashboard/live/live_match_state.json",
        "r"
    ) as f:

        state = json.load(f)

except:

    st.warning(
        "Waiting for match data..."
    )

    st.stop()

if state["innings"] == 1:

    predicted_score = None

    if state["overs_float"] > 0:

        run_rate = (
            state["score"]
            /
            state["overs_float"]
        )

        features = pd.DataFrame(
            [{
                "current_score": state["score"],
                "wickets": state["wickets"],
                "overs": state["overs_float"],
                "run_rate": run_rate
            }]
        )

        predicted_score = round(
            SCORE_MODEL.predict(
                features
            )[0]
        )

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
    )

else:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Score",
        f"{state['score']}/{state['wickets']}"
    )

    c2.metric(
        "Overs",
        state["display_over"]
    )

    c3.metric(
        "Target",
        state["target"]
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Runs Needed",
        state["runs_needed"]
    )

    c5.metric(
        "Balls Remaining",
        state["balls_remaining"]
    )

    c6.metric(
        "Required RR",
        state["required_rr"]
    )

    st.divider()

    if not state.get(
        "match_finished",
        False
    ):

        st.subheader(
            "Win Probability"
        )

        st.progress(
            state["win_probability"] / 100
        )

        st.metric(
            "Batting Team Win %",
            f"{state['win_probability']}%"
        )

        st.metric(
            "Bowling Team Win %",
            f"{100 - state['win_probability']}%"
        )

    else:

        st.subheader(
            "Match Result"
        )

        if state["runs_needed"] <= 0:

            st.success(
                "🏆 Chasing Team Won"
            )

        else:

            st.error(
                "🏆 Defending Team Won"
            )

st.divider()

st.subheader(
    "Current Delivery"
)

st.write(
    f"Over {state['display_over']}"
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