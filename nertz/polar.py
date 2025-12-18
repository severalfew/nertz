from nertz.data import read_data, make_tall
from nertz.style import colormap, player_cols
import numpy as np
import pandas as pd
import plotly.graph_objects as go


def plot_polar(df):
    df = df.copy()
    df.rename(columns={"Phil": "Phil+Becca"}, inplace=True)
    pc = {
        "Stu+Teresa": [],
        "Joan": [],
        "Mo": [],
        "Radmar": [],
        "Phil+Becca": [],
        "ThiThoa": [],
    }
    df["Month"] = df.Date.apply(lambda x: x.month)
    fig = go.Figure()
    for i in range(1, 13):
        grp = df[df.Month == i]
        for player, array in pc.items():
            cols = ["Stu", "Teresa"]
            if player != "Stu+Teresa":
                cols += [player]
            array.append((~pd.isna(grp[cols]).any(axis=1)).sum())
    pc["All-Star Break (US)"] = [10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for player, array in pc.items():
        fig.add_trace(go.Barpolar(r=array, name=player, marker_color=colormap[player]))
    fig.update_layout(
        title_text="Number of Games per Month with Each Guest",
        template=None,
        polar=dict(
            angularaxis=dict(
                tickvals=np.linspace(0, 360, 13)[:-1],
                ticktext=[
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
            )
        ),
    )
    return fig


if __name__ == "__main__":
    plot_polar(read_data()).show()
