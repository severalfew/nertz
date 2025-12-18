from data import read_data
import plotly.graph_objects as go


def plot_cumulative(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(y=df["Running Total"], mode="lines", name="Total", showlegend=True)
    )
    fig.update_layout(
        template="ggplot2",
    )
    return fig


if __name__ == "__main__":
    df = read_data()
    plot_cumulative(df).show()
