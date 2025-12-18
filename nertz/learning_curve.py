from nertz.style import colormap
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as ss


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
