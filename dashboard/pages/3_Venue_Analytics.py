import streamlit as st
import plotly.express as px

from queries import venue_analysis

st.title("🏟 Venue Analytics")

df = venue_analysis()

st.dataframe(df)

fig = px.bar(
    df,
    x="venue",
    y="matches",
    title="Matches By Venue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)