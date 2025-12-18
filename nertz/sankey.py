from nertz.style import colormap
import plotly.graph_objects as go


def plot_sankey(df):
    labels = [x for x in df.Winner.unique()]
    colors = [colormap[x] for x in labels]
    values = []
    source = []
    target = []
    for (winner, nxt), value in df.groupby(["Winner", "Next"])["index"].count().items():
        values.append(value)
        source.append(labels.index(winner))
        target.append(labels.index(nxt))
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=colors,
                ),
                link=dict(
                    arrowlen=15,
                    source=source,
                    target=target,
                    value=values,
                    color=[colormap[labels[x]] for x in target],
                ),
            )
        ]
    )

    fig.update_layout(font_size=20)
    return fig
