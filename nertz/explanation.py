from nertz.data import make_stats, player_cols, read_data
from nertz.style import enhanced_markdown
import streamlit as st


def render() -> None:
    df = read_data()
    stats = make_stats(df)

    st.subheader("Explanation")
    enhanced_markdown("explanation.md", **stats)

    st.subheader("Nertz Data")
    enhanced_markdown("dataset.md")
    st.write(df[["Date", "Nertz"] + player_cols(df)])
