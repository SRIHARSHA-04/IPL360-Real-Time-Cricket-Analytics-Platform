import streamlit as st
import plotly.express as px

from queries import team_wins

st.title("🏆 Team Analytics")

df = team_wins()

st.dataframe(df)

fig = px.bar(
    df,
    x="winner",
    y="wins",
    title="Team Wins"
)

st.plotly_chart(
    fig,
    use_container_width=True
)