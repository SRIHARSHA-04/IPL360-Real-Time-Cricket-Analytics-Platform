import streamlit as st
import plotly.express as px

from queries import (
    top_run_scorers,
    top_wicket_takers,
    team_wins,
    venue_analysis
)

st.set_page_config(
    page_title="IPL360",
    layout="wide"
)

st.title("🏏 IPL360 Analytics Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Run Scorers",
        "Wicket Takers",
        "Team Wins",
        "Venues"
    ]
)

if page == "Run Scorers":

    df = top_run_scorers()

    st.subheader("Top Run Scorers")

    st.dataframe(df)

    fig = px.bar(
        df,
        x="batter",
        y="runs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

elif page == "Wicket Takers":

    df = top_wicket_takers()

    st.subheader("Top Wicket Takers")

    st.dataframe(df)

    fig = px.bar(
        df,
        x="bowler",
        y="wickets"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

elif page == "Team Wins":

    df = team_wins()

    st.subheader("Team Wins")

    st.dataframe(df)

    fig = px.bar(
        df,
        x="winner",
        y="wins"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    df = venue_analysis()

    st.subheader("Venue Analysis")

    st.dataframe(df)

    fig = px.bar(
        df,
        x="venue",
        y="matches"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )