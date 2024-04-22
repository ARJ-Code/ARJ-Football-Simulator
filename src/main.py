import os
import pandas as pd
from football_tools.line_up import ProveLineUp, ProveLineUpGrid
from football_agent.football_agent import Player, Manager
from football_agent.strategies import RandomStrategy
from football_agent.manager_strategy import RandomStrategy as RandomStrategyManager
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

home_d = TeamData(home_n, home)
away_d = TeamData(away_n, away)

home_a = TeamAgent(
    home_n, Manager(RandomStrategyManager(), 'H', home_d.data.values()), {p.dorsal: Player(50, p.dorsal, 'H', RandomStrategy()) for p in home})
away_a = TeamAgent(
    away_n, Manager(RandomStrategyManager(), 'A', away_d.data.values()), {p.dorsal: Player(50, p.dorsal, 'A', RandomStrategy()) for p in away})

sim = FootballSimulation((home_a, home_d), (away_a, away_d))


def clear_console():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ["ce", "nt", "dos"]:
        os.system("cls")


a = time.time()
for s in sim.simulate():
    # pass
    time.sleep(0.1)
    clear_console()
    print(s)

print(abs(a-time.time()))
