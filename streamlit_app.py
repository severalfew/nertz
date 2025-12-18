from nertz.badges import assign_badges
from nertz.candlestick import plot_candlestick
from nertz.cumulative import plot_cumulative
from nertz.distributions import plot_distributions, plot_warmup
from nertz.histograms import plot_histogram, plot_marginal_histogram, plot_ecdf
from nertz.learning_curve import plot_learning, plot_learning_relation
from nertz.pie import plot_piechart
from nertz.polar import plot_polar
from nertz.sankey import plot_sankey
from nertz.sunburst import plot_sunburst
from nertz.ternary import plot_ternary, plot_distributions_versus_third
from nertz.violin import plot_thumb_comparison, plot_violin
from nertz.data import make_tall, make_stats, read_data, parse_players, player_cols
from nertz.style import enhanced_markdown
import streamlit as st

df = read_data()
players = parse_players()
assign_badges(df, players)
tall = make_tall(df)
stats = make_stats(df)

st.set_page_config(
    page_title="Nertz", layout="wide", initial_sidebar_state=None, menu_items=None
)
st.title("A Statistical Analysis of Nertz")

st.subheader("Explanation")
enhanced_markdown("explanation.md", **stats)

st.subheader("Nertz Data")
enhanced_markdown("dataset.md")
st.write(df[["Date", "Nertz"] + player_cols(df)])

st.subheader("Learning Curve")
enhanced_markdown(
    """Teresa and Stu played **many** more games of Nertz than anyone else who came to visit. Let's take a look at all
the players who do not play Nertz regularly. How did they fare over the course of several games? My hypothesis was that
we would generally see a positive trend as players warmed-up or gained experience. Here we plot each player's score in
sequential order, ignoring any gaps in time between games. For example, Radmar and Joan each visited more than once,
with gaps between the visits."""
)
st.plotly_chart(plot_learning(tall))
enhanced_markdown(
    """
About half of players showed a general improvement, but the other half show a regressive trend. In fact, high-scoring
players are more likely to show a decrease in score over time. We throw out all players with fewer than 8 games and plot
the slope vs y-intercept of the rest. The higher your y-intercept (score on your first game), the more likely your
scores are to regress down to a lower value.
"""
)
st.plotly_chart(plot_learning_relation(tall))
enhanced_markdown(
    """
From this, we can draw several conclusions:

- If players improve from experience, the window to see improvement is wider than 10-20 games.
- The data are likely too noisy, too few, or both to make any real judgement about player skill over time.
- All players regress toward some average. Even Teresa and Stu over hundreds of games show very little difference in points.
"""
)

st.plotly_chart(plot_ecdf(tall))
st.plotly_chart(plot_cumulative(df))
st.plotly_chart(plot_piechart(df))
st.plotly_chart(plot_histogram(df))
st.plotly_chart(plot_distributions(df))
st.plotly_chart(plot_candlestick(df))
st.plotly_chart(plot_thumb_comparison(df))
st.plotly_chart(plot_violin(tall))
st.plotly_chart(plot_polar(df))
st.plotly_chart(plot_marginal_histogram(df))
st.plotly_chart(plot_sankey(df))
st.plotly_chart(plot_ternary(df))
st.plotly_chart(plot_distributions_versus_third(df))
st.plotly_chart(plot_warmup(df))
st.plotly_chart(plot_sunburst(df))

st.subheader("Who's Who?")

for player in players:
    player.card()
