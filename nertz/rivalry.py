from dataclasses import dataclass
from nertz.data import read_data, parse_players
from nertz.style import colormap, player_cols
import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def plot_sunburst(df: pd.DataFrame) -> go.Figure:
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


rt = "Running Total"


def transform_for_candlestick(df: pd.DataFrame) -> tuple[pd.DataFrame, list, list]:
    curr_date = df.Date.min()
    date = curr_date
    i = 0
    dates = []
    days = []
    open_vals = []
    high = []
    low = []
    close = []
    dividers = [0]
    months = []
    stu_run = []
    stu_current_run = []
    teresa_run = []
    teresa_current_run = []
    for i, (date, grp) in enumerate(df.groupby("Date")):
        dates.append(date)
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
    values = pd.DataFrame(
        {
            "Day": days,
            "Open": open_vals,
            "High": high,
            "Low": low,
            "Close": close,
            "Date": dates,
        }
    )
    values["Margin"] = values["Close"] - values["Open"]
    return values, months, dividers


def add_guests(
    fig: go.Figure, data: pd.DataFrame, transformed: pd.DataFrame
) -> go.Figure:
    # Add info for which players played on a given day
    sub = pd.merge(
        transformed,
        (
            data.set_index("Date").groupby("Date")[player_cols(data)].count() > 0
        ).reset_index(),
    )
    for i, row in sub.iterrows():
        if row["Phil"] & row["Becca"]:
            player = "Phil+Becca"
        elif row["Tri"] & row["David"]:
            player = "David+Tri"
        else:
            player = None
            for p in parse_players():
                if not row[p.name]:
                    continue
                player = p.name
        if not player:
            continue
        date = row["Date"]
        fig.add_vrect(
            x0=transformed[transformed.Date == date].Day.iloc[0] - 0.5,
            x1=transformed[transformed.Date == date].Day.iloc[0] + 0.5,
            fillcolor=colormap[player],
        )
    return fig


def plot_candlestick(df: pd.DataFrame) -> go.Figure:
    data, months, dividers = transform_for_candlestick(df)
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=data["Day"],
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
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
        x1=len(data),
        y1=0,
        line=dict(color="#bc80bd", width=2),
    )

    teresa_best = data.loc[data["Margin"].idxmax()]
    fig.add_annotation(
        x=teresa_best["Day"],
        y=teresa_best["Close"],
        text=f"Teresa's biggest day: {teresa_best["Margin"]:.0f} pts",
        font=dict(color=colormap["Teresa"]),
        showarrow=True,
        arrowhead=0,
        ay=-30,
        ax=0,
    )

    stu_best = data.loc[data["Margin"].idxmin()]
    fig.add_annotation(
        x=stu_best["Day"],
        y=stu_best["Close"],
        text=f"Stu's biggest day: {abs(stu_best["Margin"]):.0f} pts",
        font=dict(color=colormap["Stu"]),
        showarrow=True,
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

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[x.strftime("%B") for x in months],
        ),
        xaxis_rangeslider_visible=False,
        xaxis_showgrid=False,
        yaxis_title=rt,
        template="ggplot2",
        title_text="Running Score Totals per Day",
    )
    fig.add_annotation(
        x=len(data),
        y=10,
        text=f"Teresa is winning 🡅",
        xanchor="right",
        yanchor="bottom",
        font=dict(color=colormap["Teresa"]),
        showarrow=False,
    )
    fig.add_annotation(
        x=len(data),
        y=-10,
        text=f"Stu is winning 🡇",
        xanchor="right",
        yanchor="top",
        font=dict(color=colormap["Stu"]),
        showarrow=False,
    )
    add_guests(fig, df, data)
    return fig


def render() -> None:
    data = read_data()
    st.subheader("Teresa vs Stu")
    # st.plotly_chart(plot_sunburst(data))
    st.plotly_chart(plot_candlestick(data))
