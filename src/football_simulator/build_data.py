import pandas as pd
from typing import Dict, List
from football_tools.data import PlayerData
from football_agent.player_agent import Player
from football_agent.manager_agent import Manager
from football_agent.player_strategy import DefensorStrategy, FootballStrategy, MidfielderStrategy, OfensorStrategy, RandomStrategy
from football_agent.manager_line_up_strategy import LineUpRandomStrategy, LineUpSimulateStrategy
from football_agent.manager_action_strategy import ActionRandomStrategy, ActionSimulateStrategy
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
        home_n, Manager(LineUpRandomStrategy(), ActionRandomStrategy(), 'H'), {p.dorsal: Player(50, p.dorsal, 'H', FootballStrategy()) for p in home})
    away_a = TeamAgent(
        away_n, Manager(LineUpRandomStrategy(), ActionRandomStrategy(), 'A'), {p.dorsal: Player(50, p.dorsal, 'A', FootballStrategy()) for p in away})

    sim = FootballSimulation((home_a, home_d), (away_a, away_d))

    return sim

# def conf_team(team: str, team_data: TeamData, players: List[PlayerData]) -> Dict[int, Player]:
#     team = {}
#     for p in players:
#         player_function = team_data.line_up.get_player_function(p.dorsal)
#         if player_function == ATTACK:
#             team[p.dorsal] = Player(p.mentality_vision, p.dorsal, team, OfensorStrategy())
#         elif player_function == MIDFIELD:
#             team[p.dorsal] = Player(p.mentality_vision, p.dorsal, team, MidfielderStrategy())
#         else:
#             team[p.dorsal] = Player(p.mentality_vision, p.dorsal, team, DefensorStrategy())
    
#     return team
