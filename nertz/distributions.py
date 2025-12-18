from plotly.graph_objs import Figure
import plotly.figure_factory as ff
from data import read_data, parse_players
from style import colormap, player_cols, plotly_to_html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_distributions(df):
    fig = go.Figure(
        layout=go.Layout(
            height=800,
            width=800,
            template="ggplot2",
        )
    )
    df = df.copy()
    df = df[df.Winner.isin(["Stu", "Teresa", "Draw"])]
    for ind, grp in df.groupby("Winner"):
        fig.add_trace(
            go.Scatter(
                x=grp.Stu,
                y=grp.Teresa,
                marker_color=colormap[ind],
                opacity=0.7,
                mode="markers",
                name=ind,
            )
        )
    cols = player_cols(df)
    min_score = df[cols].min().min()
    max_score = df[cols].max().max()
    fig.add_shape(
        type="line",
        x0=min_score,
        y0=min_score,
        x1=max_score,
        y1=max_score,
        line=dict(color="#bc80bd", width=3, dash="dot"),
    )

    big_win_t = df.loc[df.Marginal.idxmax()]
    fig.add_annotation(
        x=big_win_t["Stu"],
        y=big_win_t["Teresa"],
        text=f"Teresa's biggest win: {big_win_t.Teresa} to {big_win_t.Stu} <br>{big_win_t['Date']}",
        showarrow=True,
        arrowhead=0,
        ay=-30,
    )

    big_win_s = df.loc[df.Marginal.idxmin()]
    fig.add_annotation(
        x=big_win_s["Stu"],
        y=big_win_s["Teresa"],
        text=f"Stu's biggest win: {big_win_s.Stu} to {big_win_s.Teresa} <br>{big_win_s['Date']}",
        showarrow=True,
        arrowhead=0,
        ay=30,
    )

    joint_win = df.loc[(df.Stu + df.Teresa).idxmax()]
    fig.add_annotation(
        x=joint_win["Stu"],
        y=joint_win["Teresa"],
        text=f"Highest-scoring Game: {joint_win.Stu} to {joint_win.Teresa} <br>{joint_win['Date']}",
        showarrow=True,
        arrowhead=0,
        ay=-30,
    )

    joint_loss = df.loc[(df.Stu + df.Teresa).idxmin()]
    fig.add_annotation(
        x=joint_loss["Stu"],
        y=joint_loss["Teresa"],
        text=f"Lowest-scoring Game: {joint_loss.Stu} to {joint_loss.Teresa} <br>{joint_loss['Date']}",
        showarrow=True,
        arrowhead=0,
        ay=30,
    )

    fig.update_layout(
        title_text="Margin of Victory", margin=dict(b=100, t=100, l=100, r=100)
    )
    fig.update_xaxes(constrain="domain")
    fig.update_yaxes(scaleanchor="x")
    return fig


def plot_warmup(df):
    col = "Game of Day"
    df[col] = df.groupby("Date")["index"].cumcount() + 1
    tall = df[player_cols(df) + [col]].melt(
        id_vars=col, value_vars=player_cols(df), value_name="Score", var_name="Player"
    )
    norm = tall.groupby(["Player", col, "Score"])
    norm = pd.DataFrame({"Count": norm["Score"].count()}).reset_index()
    fig = px.scatter(
        norm,
        x=col,
        y="Score",
        color="Player",
        trendline="lowess",
        size="Count",
        template="ggplot2",
        color_discrete_map=colormap,
        marginal_y="box",
    )
    return fig


if __name__ == "__main__":
    plot_distributions(read_data()).show()
