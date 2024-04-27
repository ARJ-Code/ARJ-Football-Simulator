from football_simulator.build_data import conf_game
from football_simulator.simulation_params import SimulationParams
from football_llm.conf_game_llm import conf_game_llm

import os
import time
import pandas as pd

df = pd.read_csv('data/players_22.csv')

params = conf_game_llm(input(
    """
Describe tu simulación, especifica: 
* liga
* equipo local
* equipo visitante
* estrategia del manager local para elegir la alineación
* estrategia del manager visitante para elegir la alineación

"""), df)

if params is None:
    print('No se pudo inferir los parámetros de la simulación')
    exit()


print('Simulación configurada correctamente')
# params = SimulationParams('FC Barcelona', 'Real Madrid CF')

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
