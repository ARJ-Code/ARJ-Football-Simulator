import os
from football_simulator.build_data import conf_game
import time


home_n = 'FC Barcelona'
away_n = 'Real Madrid CF'

sim = conf_game(home_n, away_n)


def clear_console():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ["ce", "nt", "dos"]:
        os.system("cls")


a = time.time()
for s in sim.simulate():
    # time.sleep(0.5)
    clear_console()
    print(s)

print(abs(a-time.time()))

# from football_llm.llm import query

# print(query('hola'))
