from abc import ABC, abstractmethod
from models import Player
import numpy as np
import pandas as pd
import scipy.stats as stats


class Badge(ABC):
    @abstractmethod
    def assign(self, df: pd.DataFrame, players: list[Player]):
        pass


class HighestScore(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        max_score = 0
        p = None
        for player in players:
            score = df[player.name].dropna().max()
            if score > max_score:
                p = player
                max_score = score
        p.facts.append(f"Highest Score in a Single Game: {max_score}")


class MostGames(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        most_games = 0
        p = None
        for player in players:
            games = len(df[player.name].dropna())
            if games > most_games:
                p = player
                most_games = games
        p.facts.append(f"Most Games Played: {most_games}")


class MostDaysPlayed(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        most_days = 0
        p = None
        for player in players:
            days = len(df[~pd.isna(df[player.name])].Date.unique())
            if days > most_days:
                p = player
                most_days = days
        p.facts.append(f"Most Days Played: {most_days}")


class TightestDistribution(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_sigma = np.inf
        p = None
        for player in players:
            sigma = np.std(df[player.name].dropna())
            if sigma < best_sigma:
                p = player
                best_sigma = sigma
        p.facts.append(f"Tightest Distribution: Std Dev {best_sigma:.2f}")


class MostConsistentScore(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_range = np.inf
        p = None
        best_high = 0
        best_low = 0
        for player in players:
            vals = df[player.name].dropna()
            high, low = vals.max(), vals.min()
            if high - low < best_range:
                p = player
                best_range = high - low
                best_high = high
                best_low = low
        p.facts.append(f"Most Consistent Score: {best_high} <-> {best_low}")


class MostImproved(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_slope = 0
        p = None
        for player in players:
            vals = df[player.name].dropna()
            if len(vals) < 2:
                continue
            m, b, _, _, _ = stats.linregress(range(len(vals)), vals)
            if m > best_slope:
                p = player
                best_slope = m
        p.facts.append(f"Most Improved: +{best_slope:.2f} pts each game")


class BestDay(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_percentage = 0
        p = None
        for player in players:
            vals = df.dropna(subset=[player.name])
            if vals.Date.nunique() < 2:
                continue
            best_day = vals.groupby("Date")[player.name].mean().max()
            avg_day = vals[player.name].mean()
            percentage = best_day / avg_day
            if percentage > best_percentage:
                p = player
                best_percentage = percentage
        p.facts.append(f"Best Day: +{(best_percentage - 1) * 100:.2f}% pts per game")


class StuNemesis(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_mean = np.inf
        p = None
        for player in players:
            index = ~pd.isna(df[player.name])
            with_sum = df[index].Stu.sum() / (
                df[index].Teresa.sum() + df[index].Stu.sum()
            )
            without_sum = df[~index].Stu.sum() / (
                df[~index].Teresa.sum() + df[~index].Stu.sum()
            )
            mean = with_sum - without_sum
            if mean < best_mean:
                p = player
                best_mean = mean
        p.facts.append(f"Nemesis: {best_mean*100:.2f}% pts for Stu")


class TeresaNemesis(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_mean = np.inf
        p = None
        for player in players:
            index = ~pd.isna(df[player.name])
            with_sum = df[index].Teresa.sum() / (
                df[index].Teresa.sum() + df[index].Stu.sum()
            )
            without_sum = df[~index].Teresa.sum() / (
                df[~index].Teresa.sum() + df[~index].Stu.sum()
            )
            mean = with_sum - without_sum
            if mean < best_mean:
                p = player
                best_mean = mean
        p.facts.append(f"Nemesis: {best_mean*100:.3g}% pts for Teresa")


class MostNertz(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        most_nertz = 0
        p = None
        for player in players:
            num_nertz = (df["Nertz"] == player.name).sum()
            if num_nertz > most_nertz:
                p = player
                most_nertz = num_nertz
        p.facts.append(f"Most Nertz: {most_nertz}")


class ViktorKrum(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        most_times = 0
        p = None
        for player in players:
            vals = df.dropna(subset=[player.name])
            times = ((vals.Winner == player.name) & (vals.Nertz != player.name)).sum()
            if times > most_times:
                p = player
                most_times = times
        p.facts.append(f"Viktor Krum Award: {most_times} times")


class Normal(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        best_fit = -np.inf
        p = None
        for player in players:
            vals = df[player.name].dropna()
            result = stats.shapiro(vals)
            if result.pvalue > best_fit:
                p = player
                best_fit = result.pvalue
        p.facts.append(f"Most Normal Player: confidence {best_fit:.3g}")


class Wildcard(Badge):
    def assign(self, df: pd.DataFrame, players: list[Player]):
        highest_var = -np.inf
        p = None
        for player in players:
            result = df[player.name].dropna().var()
            if result > highest_var:
                p = player
                highest_var = result
        p.facts.append(f"Wildcard: variance {highest_var:.4g}")


badges = [
    HighestScore(),
    MostGames(),
    MostDaysPlayed(),
    TightestDistribution(),
    MostConsistentScore(),
    MostImproved(),
    BestDay(),
    TeresaNemesis(),
    StuNemesis(),
    MostNertz(),
    ViktorKrum(),
    Normal(),
    Wildcard(),
]


def assign_badges(df: pd.DataFrame, players: list[Player]):
    for badge in badges:
        badge.assign(df, players)
