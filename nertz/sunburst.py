from nertz.data import read_data
from nertz.style import colormap
import plotly.graph_objects as go


def plot_sunburst(df):
    path = ["Nertz", "Winner"]
    sub = df[path].dropna().reset_index()
    sub = sub.groupby(path).count().rename(columns={"index": "count"}).reset_index()
    sub["id"] = sub.Nertz + "-" + sub.Winner

    ids = []
    labels = []
    parents = []
    colors = []
    values = []
    for name, count in sub.groupby("Nertz").sum()["count"].items():
        ids.append(name)
        labels.append(f"{name}:<br>{count} Nertz")
        parents.append("")
        colors.append(colormap[name])
        values.append(count)
    for row in sub.itertuples():
        ids.append(row.id)
        labels.append(
            f"Winner: {row.Winner}<br>Nertz: {row.Nertz}<br>{row.count} Times"
        )
        parents.append(row.Nertz)
        colors.append(colormap[row.Winner])
        values.append(row.count)

    fig = go.Figure(
        go.Sunburst(
            ids=ids,
            labels=labels,
            parents=parents,
            marker=dict(colors=colors),
            values=values,
            branchvalues="total",
        )
    )
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0), uniformtext=dict(minsize=14, mode="hide")
    )

    return fig


if __name__ == "__main__":
    plot_sunburst(read_data()).show()
