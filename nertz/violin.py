from nertz.data import read_data
from nertz.style import colormap, player_cols, plotly_to_html
import plotly.graph_objects as go


def plot_violin(tall):
    fig = go.Figure()
    tall = tall[tall["Player"].isin(["Stu", "Teresa"])]

    for i, (weekday, grp) in enumerate(tall.groupby(["Weekday"])):
        for j, (player, grpp) in enumerate(grp.groupby(["Player"])):
            player = player[0]
            fig.add_trace(
                go.Violin(
                    x=grpp["Weekday"],
                    y=grpp["Score"],
                    legendgroup=player,
                    scalegroup=player,
                    name=player,
                    side="negative" if bool(j) else "positive",
                    pointpos=0.6 * (-1 if bool(j) else 1),  # where to position points
                    line_color=colormap[player],
                    showlegend=not bool(i),
                )
            )

    fig.update_traces(
        meanline_visible=True, points="all", jitter=0.1, scalemode="count"
    )
    fig.update_layout(
        title_text="Total Score Distribution<br><i>Split by Day of the Week",
        violingap=0,
        violingroupgap=0,
        violinmode="overlay",
        template="ggplot2",
    )
    fig.update_xaxes(
        tickangle=0,
        tickmode="array",
        tickvals=list(range(0, 8)),
        ticktext=[
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ],
    )
    return fig


def plot_thumb_comparison(df):
    fig = go.Figure()
    good = df[~df["Bad Thumb"]]
    bad = df[df["Bad Thumb"]].copy()
    start = good.Teresa.mean()
    exp_drop = bad.Stu.mean()
    actual_drop = bad.Teresa.mean()
    point_loss_per_game = exp_drop - actual_drop

    fig.add_hrect(
        y0=start,
        y1=exp_drop,
        annotation_text=f"Expected drop: {start - exp_drop:.2f} points per game",
        fillcolor="#66c2a5",
        annotation_position="top left",
    )

    fig.add_hrect(
        y0=exp_drop,
        y1=actual_drop,
        annotation_text=f"Excess drop: {point_loss_per_game:.2f} points per game",
        fillcolor="#fc8d62",
        annotation_position="top left",
    )

    fig.add_trace(
        go.Violin(
            scalegroup=1,
            x=["Teresa"] * len(good),
            y=good.Teresa,
            name="Teresa with Good Thumb",
            side="negative",
            pointpos=-0.4,  # where to position points
            line_color=colormap["Teresa"],
        )
    )
    fig.add_trace(
        go.Violin(
            scalegroup=1,
            x=["Teresa"] * len(bad),
            y=bad.Teresa,
            name="Teresa with Bad Thumb",
            side="positive",
            pointpos=0.4,  # where to position points
            line_color="#e78ac3",
        )
    )

    fig.add_trace(
        go.Violin(
            scalegroup=1,
            x=["Stu"] * len(good),
            y=good.Stu,
            name="Stu during Good Thumb",
            side="negative",
            pointpos=-1.4,  # where to position points
            line_color=colormap["Stu"],
        )
    )
    fig.add_trace(
        go.Violin(
            scalegroup=1,
            x=["Stu"] * len(bad),
            y=bad.Stu,
            name="Stu during Bad Thumb",
            side="positive",
            pointpos=1.4,  # where to position points
            line_color="#fc8d62",
        )
    )

    fig.update_traces(
        meanline_visible=True, points="all", jitter=0.1, scalemode="width"
    )

    bad["Hypothetical"] = bad.Teresa + point_loss_per_game
    marginal_wins = (bad.Hypothetical > bad.Stu).sum() - (bad.Teresa > bad.Stu).sum()

    fig.add_annotation(
        x=0.4,
        y=0,
        text=f"Bad Thumb caused Teresa to lose<br>{point_loss_per_game:.2f} pts/game for {len(bad)} games = {point_loss_per_game * len(bad):.2f} total points<br>She would have won {marginal_wins} more games with a good thumb.",
        showarrow=False,
    )

    fig.update_layout(
        title_text="Good Thumb vs Bad Thumb",
        # violingap=0,
        # violingroupgap=0,
        # violinmode="overlay",
        template="ggplot2",
        yaxis=dict(range=[df[player_cols(df)].values.min() - 1, 53]),
    )
    return fig


if __name__ == "__main__":
    df = read_data()
    with open("output.html", "w", encoding="utf-8") as fp:
        plotly_to_html(fp, plot_thumb_comparison(df), True)
