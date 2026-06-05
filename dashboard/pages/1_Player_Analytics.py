import streamlit as st
import plotly.express as px

from queries import (
    top_run_scorers,
    batting_average,
    strike_rate
)

st.title("📊 Player Analytics")

tab1, tab2, tab3 = st.tabs(
    [
        "Run Scorers",
        "Batting Average",
        "Strike Rate"
    ]
)

with tab1:

    df = top_run_scorers()

    st.dataframe(df)

    fig = px.bar(
        df,
        x="batter",
        y="runs",
        title="Top Run Scorers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    df = batting_average()

    st.dataframe(df)

    fig = px.bar(
        df,
        x="batter",
        y="average",
        title="Batting Average"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:

    df = strike_rate()

    st.dataframe(df)

    fig = px.bar(
        df,
        x="batter",
        y="strike_rate",
        title="Strike Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )