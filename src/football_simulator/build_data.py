import pandas as pd
from typing import List
from football_tools.data import PlayerData
from football_agent.player_agent import Player
from football_agent.manager_agent import Manager
from football_agent.player_strategy import RandomStrategy
from football_agent.manager_line_up_strategy import RandomStrategy as RandomStrategyManager, SimulateStrategy
from football_agent.team import TeamAgent
from football_tools.data import TeamData
from football_simulator.simulator import FootballSimulation


df = pd.read_csv('data/players_22.csv')


def get_data(team: str) -> List[PlayerData]:
    data = df[df['club_name'] == team]
    return [PlayerData(p) for _, p in data.iterrows()]


def conf_game(home_n: str, away_n: str):
    home = get_data(home_n)
    away = get_data(away_n)

    home_d = TeamData(home_n, home)
    away_d = TeamData(away_n, away)

    home_a = TeamAgent(
        home_n, Manager(SimulateStrategy(), 'H'), {p.dorsal: Player(50, p.dorsal, 'H', RandomStrategy()) for p in home})
    away_a = TeamAgent(
        away_n, Manager(SimulateStrategy(), 'A'), {p.dorsal: Player(50, p.dorsal, 'A', RandomStrategy()) for p in away})

    sim = FootballSimulation((home_a, home_d), (away_a, away_d))

    return sim
