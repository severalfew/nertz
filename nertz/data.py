from nertz.models import Player
from nertz.style import player_cols, colormap
import pandas as pd
import streamlit as st


def marginal_result(row):
    pc = player_cols(row.index)
    high_scores = row[pc].loc[row == row[pc].max()].index
    if len(high_scores) > 1:
        return "Tie"
    return high_scores[0]


@st.cache_data
def make_stats(data: pd.DataFrame) -> dict:
    return {
        "games": len(data),
        "start_date": data.Date.dropna().min(),
        "end_date": data.Date.dropna().max(),
        "num_guests": len(parse_players()),
    }


@st.cache_data
def parse_players() -> list[Player]:
    names = [
        "Joan",
        "Mo",
        "Radmar",
        "Phil",
        "Becca",
        "ThiThoa",
        "David",
        "Tri",
        "Mallory",
        "Jack",
    ]
    players = []
    for name in names:
        player = Player(
            name=name,
            color=colormap[name],
        )
        players.append(player)
    return players


def read_data() -> pd.DataFrame:
    df = pd.read_csv("Nertz.csv").dropna(subset=["Date"])
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df.Date).apply(lambda x: x.date())
    df["Marginal"] = df["Teresa"] - df["Stu"]
    df[["Stu Total", "Teresa Total", "Running Total"]] = df[
        ["Stu", "Teresa", "Marginal"]
    ].cumsum()
    df["Win Margin"] = df.Marginal.abs()

    df["Winner"] = df.apply(marginal_result, axis=1)
    df["Next"] = df.Winner.shift(1)
    df["Next2"] = df.Winner.shift(2)
    df["Bad Thumb"] = df["Bad Thumb"].astype(bool)
    return df


def make_tall() -> pd.DataFrame:
    df = read_data()
    tall = df[["index", "Date"] + player_cols(df)].melt(
        id_vars=["index", "Date"], var_name="Player", value_name="Score"
    )
    tall["Weekday"] = tall.Date.apply(lambda x: x.weekday())
    return tall.dropna(subset=["Score"])
