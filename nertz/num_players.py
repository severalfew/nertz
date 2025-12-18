from nertz.style import enhanced_markdown
from nertz.data import player_cols, read_data
from nertz.style import colormap
from plotly.graph_objects import Figure, Scatter
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as ss
import streamlit as st

xcol = "Num Players"
ycol = "Difference from Mean Score"


def prepare_data() -> pd.DataFrame:
    data = read_data()
    data = data[player_cols(data)]
    data = data - data.mean()
    data[xcol] = data.apply(lambda x: x.dropna().count(), axis=1)
    data = data.melt(id_vars=[xcol], var_name="Player", value_name=ycol).dropna(
        subset=ycol
    )
    data["Num Players Jitter"] = data[xcol] + np.random.uniform(-0.1, 0.1, len(data))
    return data


def plot_num_players(data: pd.DataFrame) -> Figure:
    fig = px.scatter(
        data,
        x="Num Players Jitter",
        y=ycol,
        color="Player",
        color_discrete_map=colormap,
    )
    x0, x1 = data[xcol].min(), data[xcol].max()
    for player, grp in data.groupby("Player"):
        if grp[xcol].nunique() < 2:
            continue
        m, b, _, _, _ = ss.linregress(grp[xcol], grp[ycol])
        fig.add_trace(
            Scatter(
                x=[x0, x1],
                y=[m * x0 + b, m * x1 + b],
                name=f"{player}: m={m:.2f}",
                marker_color=colormap[player],
                mode="lines",
            )
        )

    return fig


def render() -> None:
    df = prepare_data()
    st.subheader("Number of Players")
    to_compare = []
    for player, grp in df.groupby("Player"):
        if grp[xcol].nunique() < 2:
            continue
        to_compare.append(player)
    enhanced_markdown(
        f"""
Nertz can be played with any number of players, as long as each player has their own distinguishable deck. Once, we
played with eighteen people! (Not recorded in these stats, unfortunately.) Does the number of players affect the 
expected score? We normalize each player's score by their mean, then look for a trend over the number of players in the
game. Only {', '.join(to_compare)} played with more than a single player-count."""
    )
    st.plotly_chart(plot_num_players(df))
    enhanced_markdown(
        """The slopes show that, in general, players score +5pts per additional player added to the game.
Of course, this has some upper limit (the max possible score of 52). But it does make sense, with more players adding
piles to the center and more action in general, there are more opportunities to get cards into scoring positions."""
    )
