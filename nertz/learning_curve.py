from style import colormap
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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
