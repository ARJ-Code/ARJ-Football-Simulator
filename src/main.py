import os
from football_simulator.build_data import conf_game
import time
from football_llm.conf_game_llm import conf_game_llm
import pandas as pd

df = pd.read_csv('data/players_22.csv')

params = conf_game_llm(input(
    'Describe tu simulación, especifica liga, equipo local y equipo visitante:\n'), df)

if params is None:
    print('No se pudo inferir los parámetros de la simulación')
    exit()

sim = conf_game(params, df)


def clear_console():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ["ce", "nt", "dos"]:
        os.system("cls")


for s in sim.simulate():
    time.sleep(0.5)
    clear_console()
    print(s)

