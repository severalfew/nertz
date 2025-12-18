from data import read_data
from style import colormap, player_cols
from scipy.spatial import ConvexHull
import numpy as np
import plotly.graph_objects as go
import pandas as pd

cols = ["Third", "Teresa", "Stu"]


def harmonize(row):
    rowmin = row[cols].min()
    if rowmin >= 1:
        return row

    for col in cols:
        row[col] += 20
    return row


def make_axis(title, tickangle):
    return {
        "title": title,
        # "titlefont": {"size": 20},
        "tickangle": tickangle,
        "tickfont": {"size": 15},
        "tickcolor": "rgba(0,0,0,0)",
        "ticklen": 5,
        "showline": True,
        "showgrid": True,
    }


def simplex_unravel(array: np.array) -> np.array:
    # Re-order simplices for better plotting
    start = array[0, 1]
    ignore = [0]
    edges = [array[0]]

    while len(edges) < len(array):
        for i, edge in enumerate(array):
            if i in ignore:
                continue
            if start == edge[0]:
                ignore.append(i)
                edges.append(edge)
                start = edge[1]
                break
            elif start == edge[1]:
                ignore.append(i)
                edges.append(edge[::-1])
                start = edge[0]
                break
    return np.array(edges)


def plot_ternary(df):
    norm = (
        df[player_cols(df)]
        .melt(id_vars=["Stu", "Teresa"], var_name="Player", value_name="Third")
        .dropna()
        .apply(harmonize, axis=1)
    )

    fig = go.Figure()

    fig.update_traces(
        marker=dict(size=15, opacity=0.8, line=dict(width=1.5, color="DarkSlateGrey"))
    )
    for ind, sub in norm.groupby("Player"):
        total = sub[cols].sum(axis=1)

        points = np.array([sub.Stu / total, sub.Third / total]).T
        extrema = []

        for simplex in simplex_unravel(ConvexHull(points).simplices):
            extrema.append(sub.iloc[simplex[0]])
            extrema.append(sub.iloc[simplex[1]])
        extrema = pd.concat(extrema, axis=1)
        extrema = extrema.T
        fig.add_trace(
            go.Scatterternary(
                a=extrema.Third,
                b=extrema.Teresa,
                c=extrema.Stu,
                mode="lines",
                marker=dict(color=colormap[ind]),
                line=dict(width=4),
                name=ind,
            )
        )
    # for ind, sub in norm.groupby("Player"):
    #     fig.add_trace(
    #         go.Scatterternary(
    #             a=sub.Third,
    #             b=sub.Teresa,
    #             c=sub.Stu,
    #             mode="markers",
    #             marker=dict(
    #                 color=colormap[ind],
    #                 size=15,
    #                 opacity=0.8,
    #                 line=dict(width=1.5, color="DarkSlateGrey"),
    #             ),
    #             name=ind,
    #         )
    #     )
    fig.update_layout(
        template="ggplot2",
        ternary={
            "sum": 100,
            "aaxis": make_axis("Third", 0),
            "baxis": make_axis("<br>Teresa", 30),
            "caxis": make_axis("<br>Stu", 0),
        },
    )
    return fig


def plot_distributions_versus_third(df):
    norm = (
        df[player_cols(df)]
        .melt(id_vars=["Stu", "Teresa"], var_name="Player", value_name="Third")
        .dropna()
    )
    norm = norm[norm.Player != "Becca"]
    norm["Player"] = norm.Player.replace("Phil", "Phil + Becca")
    max_y = norm[["Stu", "Teresa", "Third"]].max().max()
    fig = go.Figure()
    i = 0
    for i, (ind, grp) in enumerate(norm.groupby("Player")):
        fig.add_trace(
            go.Violin(
                x=grp["Player"],
                y=grp["Teresa"],
                legendgroup="Teresa",
                scalegroup=ind,
                name="Teresa",
                side="negative",
                line_color=colormap["Teresa"],
                pointpos=-0.5,
                showlegend=not bool(i),
                spanmode="manual",
                span=[0, 52],
            )
        )
        fig.add_trace(
            go.Violin(
                x=grp["Player"],
                y=grp["Stu"],
                legendgroup="Stu",
                scalegroup=ind,
                name="Stu",
                side="positive",
                line_color=colormap["Stu"],
                pointpos=0.5,
                showlegend=not bool(i),
                spanmode="manual",
                span=[0, 52],
            )
        )
        mean_diff = grp["Teresa"].mean() - grp["Stu"].mean()
        if mean_diff > 0:
            better = "Teresa"
        else:
            better = "Stu"
        fig.add_annotation(
            x=i,
            y=max_y + 1 if better == "Teresa" else 3,
            xref="x",
            yref="y",
            text=f"{better} scored {abs(mean_diff):.2f}<br>more points per game",
            showarrow=False,
            bgcolor=colormap.get(ind, colormap["Draw"]),
            opacity=1,
        )
    fig.update_traces(
        meanline_visible=True, points="all", jitter=0.05, scalemode="count"
    )
    fig.update_layout(
        violingap=0,
        violingroupgap=0.1,
        violinmode="overlay",
        xaxis_range=[-0.5, i + 0.5],
        yaxis_range=[0, 52],
    )
    return fig


if __name__ == "__main__":
    plot_ternary(read_data()).show()
