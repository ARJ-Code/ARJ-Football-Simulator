import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def fuzzy_defensive_position():
    distance_to_position = ctrl.Antecedent(np.arange(0, 20, 1), 'distance_to_position')
    distance_to_ball = ctrl.Antecedent(np.arange(0, 20, 1), 'distance_to_ball')
    player_function = ctrl.Antecedent(np.arange(0, 3, 1), 'player_function')
    defensive_position = ctrl.Consequent(np.arange(0, 100, 1), 'defensive_position')

    distance_to_position['low'] = fuzz.trimf(distance_to_position.universe, [0, 0, 2])
    distance_to_position['medium'] = fuzz.trimf(distance_to_position.universe, [1, 4, 6])
    distance_to_position['high'] = fuzz.trimf(distance_to_position.universe, [5, 20, 20])

    distance_to_ball['low'] = fuzz.trimf(distance_to_ball.universe, [0, 0, 2])
    distance_to_ball['medium'] = fuzz.trimf(distance_to_ball.universe, [1, 6, 10])
    distance_to_ball['high'] = fuzz.trimf(distance_to_ball.universe, [8, 20, 20])

    player_function['defense'] = fuzz.trimf(player_function.universe, [0, 0, 1])
    player_function['midfield'] = fuzz.trimf(player_function.universe, [0, 1, 2])
    player_function['attack'] = fuzz.trimf(player_function.universe, [1, 2, 2])

    defensive_position['bad'] = fuzz.trimf(defensive_position.universe, [0, 0, 50])
    defensive_position['normal'] = fuzz.trimf(defensive_position.universe, [0, 50, 100])
    defensive_position['good'] = fuzz.trimf(defensive_position.universe, [50, 100, 100])

    rule1 = ctrl.Rule(distance_to_ball['low'], defensive_position['good'])
    rule2 = ctrl.Rule(distance_to_position['low'] & player_function['defense'], defensive_position['good'])
    rule3 = ctrl.Rule(distance_to_position['high'] & player_function['defense'], defensive_position['bad'])
    rule4 = ctrl.Rule(distance_to_ball['high'] & player_function['midfield'], defensive_position['bad'])
    rule5 = ctrl.Rule(distance_to_ball['high'] & player_function['attack'], defensive_position['normal'])

    defensive_position_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    defensive_positioning = ctrl.ControlSystemSimulation(defensive_position_ctrl)

    return defensive_positioning

def fuzzy_ofensive_position():
    distance_to_position = ctrl.Antecedent(np.arange(0, 20, 1), 'distance_to_position')
    distance_to_enemy_goal = ctrl.Antecedent(np.arange(0, 20, 1), 'distance_to_enemy_goal')
    distance_to_ball = ctrl.Antecedent(np.arange(0, 20, 1), 'distance_to_ball')
    player_function = ctrl.Antecedent(np.arange(0, 3, 1), 'player_function')
    ofensive_position = ctrl.Consequent(np.arange(0, 100, 1), 'ofensive_position')

    distance_to_position['low'] = fuzz.trimf(distance_to_position.universe, [0, 0, 2])
    distance_to_position['medium'] = fuzz.trimf(distance_to_position.universe, [1, 4, 6])
    distance_to_position['high'] = fuzz.trimf(distance_to_position.universe, [5, 20, 20])

    distance_to_enemy_goal['low'] = fuzz.trimf(distance_to_enemy_goal.universe, [0, 0, 3])
    distance_to_enemy_goal['medium'] = fuzz.trimf(distance_to_enemy_goal.universe, [2, 4, 7])
    distance_to_enemy_goal['high'] = fuzz.trimf(distance_to_enemy_goal.universe, [6, 20, 20])

    distance_to_ball['low'] = fuzz.trimf(distance_to_ball.universe, [0, 0, 2])
    distance_to_ball['medium'] = fuzz.trimf(distance_to_ball.universe, [1, 6, 10])
    distance_to_ball['high'] = fuzz.trimf(distance_to_ball.universe, [8, 20, 20])

    player_function['defense'] = fuzz.trimf(player_function.universe, [0, 0, 1])
    player_function['midfield'] = fuzz.trimf(player_function.universe, [0, 1, 2])
    player_function['attack'] = fuzz.trimf(player_function.universe, [1, 2, 2])

    ofensive_position['bad'] = fuzz.trimf(ofensive_position.universe, [0, 0, 50])
    ofensive_position['normal'] = fuzz.trimf(ofensive_position.universe, [0, 50, 100])
    ofensive_position['good'] = fuzz.trimf(ofensive_position.universe, [50, 100, 100])

    rule1 = ctrl.Rule(distance_to_ball['high'] & distance_to_enemy_goal['high'], ofensive_position['bad'])
    rule2 = ctrl.Rule(~distance_to_ball['high'] & player_function['midfield'], ofensive_position['good'])
    rule3 = ctrl.Rule(distance_to_position['low'] & ~distance_to_ball['high'], ofensive_position['good'])
    rule4 = ctrl.Rule(distance_to_enemy_goal['high'] & player_function['attack'], ofensive_position['bad'])

    ofensive_position_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
    ofensive_positioning = ctrl.ControlSystemSimulation(ofensive_position_ctrl)

    return ofensive_positioning
