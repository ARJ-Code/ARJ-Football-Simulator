import pandas as pd
from football_agent.football_agent import Player
from football_agent.strategies import RandomStrategy
from football_agent.team import TeamAgent
from football_tools.data import TeamData
from football_simulator.build_data import get_data
from football_simulator.simulation import FootballSimulation
import time

df = pd.read_csv('data/players_22.csv')
home_n = 'FC Barcelona'
away_n = 'Real Madrid CF'

home = get_data(home_n)
away = get_data(away_n)

home_line_up = [(10, 6, 8), (9, 6, 5), (7, 6, 2),
                (21, 11, 8), (5, 11, 5), (14, 11, 2), (20, 15, 8), (4, 15, 6), (3, 15, 4), (18, 15, 2), (1, 18, 5)]
away_line_up = [(21, 13, 2), (9, 13, 5), (20, 13, 8), (10, 8, 8), (14, 8, 5),
                (8, 8, 2), (2, 4, 2), (3, 4, 4), (4, 4, 6), (23, 4, 8), (1, 1, 5)]

home_d = TeamData(home_n, home_line_up, home)
away_d = TeamData(away_n, away_line_up, away)

home_a = TeamAgent(
    home_n, {p.dorsal: Player(50, p.dorsal, 'H', RandomStrategy()) for p in home})
away_a = TeamAgent(
    away_n, {p.dorsal: Player(50, p.dorsal, 'A', RandomStrategy()) for p in away})

sim = FootballSimulation((home_a, home_d), (away_a, away_d))

import os

def clear_console():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ["ce", "nt", "dos"]:
        os.system("cls")

a = time.time()
for s in sim.simulate():
    pass
    # time.sleep(0.5)
    # clear_console()
    # print(s)
    
print (abs(a-time.time()))