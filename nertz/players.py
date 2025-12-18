from nertz.badges import assign_badges
from nertz.data import parse_players, read_data
from nertz.style import enhanced_markdown
import streamlit as st

def render() -> None:
    df = read_data()
    players = parse_players()
    assign_badges(df, players)

    st.subheader("Play Styles")
    enhanced_markdown("""
What can we say about individual players and their styles?
""")

    for player in players:
        player.card()
