from nertz.style import colormap
import plotly.express as px


def plot_piechart(df):
    count = df.groupby("Winner")["Marginal"].count().reset_index()
    fig = px.pie(
        count,
        values="Marginal",
        names="Winner",
        color="Winner",
        color_discrete_map=colormap,
        width=500,
        height=500,
        template="ggplot2",
    )
    fig.update_traces(textposition="inside", textinfo="value+percent+label")
    fig.update_layout(title_text="Total Games Won", uniformtext_minsize=20)
    return fig
