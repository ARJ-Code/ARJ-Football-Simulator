from football_simulator.build_data import conf_game

import pandas as pd
from params import *
import json
import time

class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"

df = pd.read_csv('data/players_22.csv')

params = [all_random, 
          all_smart, 
          smart_line_up, 
          smart_vs_random_line_up, 
          smart_action, 
          smart_vs_random_action, 
          smart_player, 
          smart_vs_random_player]

initial_time = time.time()

for p in params:
    try:
        data = {}
        file_name = f"data/{p.name}.json"
        for i in range(30):
            sim = conf_game(p.simulation_params, df)
            s = sim.simulate_and_save()
            data[i] = s

        with open(file_name, "w") as archivo:
            json.dump(s, archivo)

        actual_time = time.time()

        print(Color.GREEN + f'Finished {p.name} simulation in {actual_time - initial_time} seconds' + Color.RESET)
        initial_time = actual_time
    except Exception as e:
        actual_time = time.time()

        print(Color.RED + f'Error in {p.name} simulation: {e} in {actual_time - initial_time} seconds' + Color.RESET)
        initial_time = actual_time
        continue