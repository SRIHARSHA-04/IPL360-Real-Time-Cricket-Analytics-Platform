import json
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st_autorefresh(
    interval=500,
    key="live_refresh"
)

st.set_page_config(
    page_title="IPL360 Live Match Center",
    layout="wide"
)

st.title("🏏 IPL360 Live Match Center")

try:

    with open(
        "dashboard/live/live_match_state.json",
        "r"
    ) as f:

        state = json.load(f)

except:

    st.warning("Waiting for match data...")
    st.stop()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Innings",
    state["innings"]
)

c2.metric(
    "Score",
    state["score"]
)

c3.metric(
    "Wickets",
    state["wickets"]
)

c4.metric(
    "Overs",
    state["display_over"]
)

st.divider()

st.subheader("Current Delivery")

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