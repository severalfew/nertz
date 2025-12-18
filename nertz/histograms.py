from data import read_data
from plotly.graph_objects import Figure
from style import colormap, player_cols
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


def plot_histogram(data: pd.DataFrame) -> Figure:
    datas = []
    labels = []
    colors = []
    for player in player_cols(data):
        datas.append(data[player].dropna())
        labels.append(player)
        colors.append(colormap[player])
    fig = ff.create_distplot(
        datas, labels, show_hist=False, show_rug=False, colors=colors
    )
    fig.update_layout(title_text="Player Score Distributions", xaxis_title="Score")
    return fig


def plot_ecdf(tall: pd.DataFrame) -> Figure:
    fig = px.ecdf(
        tall,
        y="Score",
        color="Player",
        markers=True,
        lines=True,
        marginal="box",
        ecdfnorm="percent",
        color_discrete_map=colormap,
        template="ggplot2",
        # orientation="h"
    )
    fig.update_layout(title_text="Player Score Distributions")
    return fig


def plot_marginal_histogram(df):
    max_score = df[player_cols(df)].max().max()
    min_score = df[player_cols(df)].min().min()
    fig = px.histogram(
        df,
        x="Marginal",
        color="Winner",
        marginal="box",
        color_discrete_map=colormap,
        nbins=int(2 * (max_score - min_score)),
        range_x=[df.Marginal.min() - 0.5, df.Marginal.max() + 0.5],
        template="ggplot2",
    )
    fig.update_layout(title_text="Win Distributions")
    return fig


if __name__ == "__main__":
    plot_marginal_histogram(read_data()).show()
