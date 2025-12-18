from nertz.data import read_data
from nertz.style import colormap
from dataclasses import dataclass
import datetime
import pandas as pd
import plotly.graph_objects as go


@dataclass
class DailyResult:
    date: datetime.date
    margin: int
    open_val: int
    close_val: int
    index: int


def plot_candlestick(df: pd.DataFrame) -> go.Figure:
    rt = "Running Total"
    curr_date = df.Date.min()
    days = []
    open_vals = []
    high = []
    low = []
    close = []
    fig = go.Figure()
    stu_best = DailyResult(index=0, date=curr_date, margin=0, open_val=0, close_val=0)
    teresa_best = DailyResult(
        index=0, date=curr_date, margin=0, open_val=0, close_val=0
    )
    dividers = [0]
    months = []
    stu_run = []
    stu_current_run = []
    teresa_run = []
    teresa_current_run = []
    for i, (date, grp) in enumerate(df.groupby("Date")):
        days.append(i)
        try:
            open_val = df[rt].loc[grp.index[0] - 1]
        except KeyError:
            open_val = 0
        open_vals.append(open_val)
        high_val = max(open_val, grp[rt].max())
        high.append(high_val)
        low_val = min(open_val, grp[rt].min())
        low.append(low_val)
        close_val = grp[rt].iloc[-1]
        close.append(close_val)
        if curr_date.month != date.month:
            months.append(curr_date)
            dividers.append(i)
            curr_date = date
        margin = close[-1] - open_val
        if margin < stu_best.margin:
            stu_best = DailyResult(
                date=date,
                index=i,
                margin=margin,
                close_val=close_val,
                open_val=open_val,
            )
        elif margin > teresa_best.margin:
            teresa_best = DailyResult(
                date=date,
                index=i,
                margin=margin,
                close_val=close_val,
                open_val=open_val,
            )
        if margin < 0:
            stu_current_run.append(i)
            if len(stu_current_run) > len(stu_run):
                stu_run = stu_current_run
            teresa_current_run = []
        else:
            teresa_current_run.append(i)
            if len(teresa_current_run) > len(teresa_run):
                teresa_run = teresa_current_run
            stu_current_run = []
    months.append(date)
    dividers.append(i + 1)

    fig.add_trace(
        go.Candlestick(
            x=days,
            open=open_vals,
            high=high,
            low=low,
            close=close,
            increasing_line_color=colormap["Teresa"],
            decreasing_line_color=colormap["Stu"],
            showlegend=True,
            name="Daily Change",
        )
    )

    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=len(days),
        y1=0,
        line=dict(color="#bc80bd", width=2),
    )

    fig.add_annotation(
        x=teresa_best.index,
        y=teresa_best.close_val,
        text=f"Teresa's biggest day: {teresa_best.margin:.0f} pts<br>{teresa_best.date}",
        showarrow=True,
        arrowhead=0,
        ay=-30,
        ax=0,
    )

    fig.add_annotation(
        x=stu_best.index,
        y=stu_best.close_val,
        text=f"Stu's biggest day: {abs(stu_best.margin):.0f} pts<br>{stu_best.date}",
        showarrow=True,
        arrowhead=0,
        ay=40,
        ax=0,
    )

    tick_vals = []
    for i, month in enumerate(months):
        fig.add_vrect(
            x0=dividers[i] - 0.5,
            x1=dividers[i + 1] - 0.5,
            fillcolor="rgba(0, 0, 0, 0.0)",
            line=dict(color="#aaaaaa", width=2),
        )
        tick_vals.append((dividers[i] + dividers[i + 1] - 1) / 2.0)

    fig.add_vrect(
        x0=stu_run[0] - 0.5,
        x1=stu_run[-1] + 0.5,
        annotation_text=f"Stu's longest run:<br>{len(stu_run)} days",
        fillcolor=colormap["Stu"],
    )

    fig.add_vrect(
        x0=teresa_run[0] - 0.5,
        x1=teresa_run[-1] + 0.5,
        annotation_text=f"Teresa's longest run:<br>{len(teresa_run)} days",
        fillcolor=colormap["Teresa"],
        annotation_position="bottom",
    )
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[x.strftime("%B") for x in months],
        ),
        xaxis_rangeslider_visible=False,
        template="ggplot2",
        title_text="Running Score Totals per Day",
    )
    fig.add_annotation(
        x=53,
        y=4,
        text=f"Teresa is winning",
        xanchor="center",
        yanchor="middle",
        font=dict(color=colormap["Teresa"]),
        showarrow=False,
    )
    fig.add_annotation(
        x=53,
        y=-4,
        text=f"Stu is winning",
        xanchor="center",
        yanchor="middle",
        font=dict(color=colormap["Stu"]),
        showarrow=False,
    )
    fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)

    return fig


if __name__ == "__main__":
    plot_candlestick(read_data()).show()
