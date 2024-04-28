from pandas import DataFrame
from typing import List
from football_tools.data import PlayerData
from football_agent.player_agent import Player
from football_agent.manager_agent import Manager
from football_agent.player_strategy import FootballStrategy, MinimaxStrategy
from football_agent.team import TeamAgent
from football_tools.data import TeamData
from football_simulator.simulator import FootballSimulation
from .simulation_params import SimulationParams
from football_tools.enum import HOME, AWAY


def get_data(team: str, df: DataFrame) -> List[PlayerData]:
    data = df[df['club_name'] == team]
    return [PlayerData(p) for _, p in data.iterrows()]


def conf_game(params: SimulationParams, df: DataFrame) -> FootballSimulation:
    home_n, away_n = params.names
    home_line_up, away_line_up = params.managers_line_up
    home_action, away_action = params.managers_action
    home_player_action, away_player_action = params.players_action_strategy
    home = get_data(home_n, df)
    away = get_data(away_n, df)

    home_d = TeamData(home_n, home)
    away_d = TeamData(away_n, away)

    home_a = TeamAgent(
        home_n, Manager(home_line_up, home_action, HOME), {p.dorsal: Player(p.mentality_vision, p.dorsal, HOME, home_player_action) for p in home})
    away_a = TeamAgent(
        away_n, Manager(away_line_up, away_action, AWAY), {p.dorsal: Player(p.mentality_vision, p.dorsal, AWAY, away_player_action) for p in away})

    sim = FootballSimulation((home_a, home_d), (away_a, away_d))

    return sim
