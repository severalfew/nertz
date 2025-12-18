from nertz.data import make_tall
from nertz.style import colormap, enhanced_markdown
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as ss
import streamlit as st


def plot_learning(tall: pd.DataFrame) -> go.Figure:
    sub = tall[~tall.Player.isin(["Stu", "Teresa"])]
    sub["Game Number"] = sub.groupby("Player").cumcount() + 1
    fig = px.scatter(
        sub,
        facet_col="Player",
        x="Game Number",
        y="Score",
        color="Player",
        color_discrete_map=colormap,
        trendline="ols",
    )
    return fig


def plot_learning_relation(tall: pd.DataFrame) -> go.Figure:
    sub = tall[~tall.Player.isin(["Stu", "Teresa"])]
    sub["Game Number"] = sub.groupby("Player").cumcount() + 1
    data = []
    for player, grp in sub.groupby("Player"):
        if len(grp.dropna(subset="Score")) < 8:
            continue
        m, b, _, _, _ = ss.linregress(grp["Game Number"], grp.Score)
        data.append([player, m, b])
    df = pd.DataFrame(data, columns=["Player", "Slope", "Y-Intercept"])
    fig = px.scatter(
        df,
        color="Player",
        x="Slope",
        y="Y-Intercept",
        trendline="ols",
        trendline_scope="overall",
        color_discrete_map=colormap,
    )
    return fig


def render() -> None:
    tall = make_tall()
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
scores are to regress down to a lower value. Sorry, Becca, your high scores were probably just a statistical anomaly!
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
