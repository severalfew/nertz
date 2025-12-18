from nertz.data import read_data
from nertz.style import colormap
import plotly.graph_objects as go
import numpy as np
import scipy.stats as ss


def plot_improvement(df):
    pc = ["Joan", "Mo", "Radmar", "Phil", "Becca", "ThiThoa", "David", "Tri"]
    pc_data = {player: df.dropna(subset=[player]) for player in pc}
    fig = go.Figure()
    for player, data in pc_data.items():
        x = np.linspace(0, 1, len(data))
        y = data[player]
        fig.add_trace(
            go.Scatter(
                x=x, y=y, name=player, mode="lines", marker_color=colormap[player]
            )
        )
        m, b, _, _, _ = ss.linregress(x, y)
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[b, m + b],
                name=f"{m:0.2f}x + {b:0.2f}",
                marker_color=colormap[player],
                mode="lines",
                line_dash="dot",
            )
        )
    fig.update_layout(title_text="Improvement over Time", template="ggplot2")
    fig.show()


if __name__ == "__main__":
    plot_improvement(read_data()).show()
