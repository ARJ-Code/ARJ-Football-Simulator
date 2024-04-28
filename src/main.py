from football_agent.manager_action_strategy import ActionRandomStrategy
from football_agent.manager_line_up_strategy import LineUpRandomStrategy
from football_agent.player_strategy import FootballStrategy, OfensorStrategy, RandomStrategy
from football_simulator.build_data import conf_game
from football_llm.conf_game_llm import conf_game_llm

import os
import time
import pandas as pd

from football_simulator.simulation_params import SimulationParams

df = pd.read_csv('data/players_22.csv')

params = conf_game_llm(input(
    """
Describe tu simulación, especifica:
* liga
* equipo local
* equipo visitante
* estrategia del manager local para elegir la alineación
* estrategia del manager visitante para elegir la alineación
* estrategias de los jugadores para tomar decisiones

"""), df)

if params is None:
    print('No se pudo inferir los parámetros de la simulación')
    exit()


print('Simulación configurada correctamente')

# params = SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
#                           (LineUpRandomStrategy(), LineUpRandomStrategy()),
#                           (ActionRandomStrategy(), ActionRandomStrategy()), 
#                           (RandomStrategy(), RandomStrategy()))

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
