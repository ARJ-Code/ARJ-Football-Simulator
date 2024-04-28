from football_agent.manager_action_strategy import *
from football_agent.manager_line_up_strategy import *
from football_agent.player_strategy import *
from football_simulator.simulation_params import SimulationParams

class StartingParams:
    def __init__(self, simulation_params, name: str):
        self.simulation_params = simulation_params
        self.name = name


all_random = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionRandomStrategy(), ActionRandomStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'all_random')

all_smart = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'),
                            (LineUpSimulateStrategy(), LineUpSimulateStrategy()),
                            (ActionSimulateStrategy(), ActionSimulateStrategy()), 
                            (FootballStrategy(), FootballStrategy())), 'all_smart')

smart_line_up = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpSimulateStrategy(), LineUpSimulateStrategy()),
                          (ActionRandomStrategy(), ActionRandomStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'smart_line_up')

smart_vs_random_line_up = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpSimulateStrategy(), LineUpRandomStrategy()),
                          (ActionRandomStrategy(), ActionRandomStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'smart_vs_random_line_up')

smart_action = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionSimulateStrategy(), ActionSimulateStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'smart_action')

smart_vs_random_action = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionRandomStrategy(), ActionSimulateStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'smart_vs_random_action')

minimax_vs_minimax_action = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionMiniMaxStrategy(), ActionMiniMaxStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'minimax_vs_minimax_action')

minimax_vs_random_action = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionMiniMaxStrategy(), ActionRandomStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'minimax_vs_random_action')

minimax_vs_smart_action = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionMiniMaxStrategy(), ActionSimulateStrategy()), 
                          (RandomStrategy(), RandomStrategy())), 'minimax_vs_smart_action')

smart_player = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionRandomStrategy(), ActionRandomStrategy()), 
                          (FootballStrategy(), FootballStrategy())), 'smart_player')

smart_vs_random_player = StartingParams(SimulationParams(('FC Barcelona', 'Real Madrid CF'), 
                          (LineUpRandomStrategy(), LineUpRandomStrategy()),
                          (ActionRandomStrategy(), ActionRandomStrategy()), 
                          (FootballStrategy(), RandomStrategy())), 'smart_vs_random_player')