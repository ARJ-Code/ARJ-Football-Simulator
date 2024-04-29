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

     

    rule1 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['defense'], defensive_position['good'])
    rule2 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['midfield'], defensive_position['good'])
    rule3 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['attack'], defensive_position['good'])

    rule4 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['defense'], defensive_position['good'])
    rule5 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['midfield'], defensive_position['normal'])
    rule6 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['attack'], defensive_position['normal'])

    rule7 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['defense'], defensive_position['normal'])
    rule8 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['midfield'], defensive_position['normal'])
    rule9 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['attack'], defensive_position['bad'])

    rule10 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['defense'], defensive_position['normal'])
    rule11 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['midfield'], defensive_position['normal'])
    rule12 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['attack'], defensive_position['normal'])

    rule13 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['defense'], defensive_position['normal'])
    rule14 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['midfield'], defensive_position['normal'])
    rule15 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['attack'], defensive_position['normal'])

    rule16 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['defense'], defensive_position['bad'])
    rule17 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['midfield'], defensive_position['bad'])
    rule18 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['attack'], defensive_position['normal'])

    rule19 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['defense'], defensive_position['bad'])
    rule20 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['midfield'], defensive_position['normal'])
    rule21 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['attack'], defensive_position['normal'])

    rule22 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['defense'], defensive_position['bad'])
    rule23 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['midfield'], defensive_position['bad'])
    rule24 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['attack'], defensive_position['normal'])

    rule25 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['defense'], defensive_position['bad'])
    rule26 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['midfield'], defensive_position['bad'])
    rule27 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['attack'], defensive_position['bad'])

    defensive_position_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, 
                                                 rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, 
                                                 rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
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

    rule1 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['defense'], ofensive_position['good'])
    rule2 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['midfield'], ofensive_position['good'])
    rule3 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['low'] & player_function['attack'], ofensive_position['good'])

    rule4 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['defense'], ofensive_position['good'])
    rule5 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['midfield'], ofensive_position['normal'])
    rule6 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['medium'] & player_function['attack'], ofensive_position['normal'])

    rule7 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['defense'], ofensive_position['normal'])
    rule8 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['midfield'], ofensive_position['bad'])
    rule9 = ctrl.Rule(distance_to_position['low'] & distance_to_ball['high'] & player_function['attack'], ofensive_position['normal'])

    rule10 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['defense'], ofensive_position['normal'])
    rule11 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['midfield'], ofensive_position['normal'])
    rule12 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['low'] & player_function['attack'], ofensive_position['normal'])

    rule13 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['defense'], ofensive_position['normal'])
    rule14 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['midfield'], ofensive_position['normal'])
    rule15 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['medium'] & player_function['attack'], ofensive_position['normal'])

    rule16 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['defense'], ofensive_position['bad'])
    rule17 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['midfield'], ofensive_position['bad'])
    rule18 = ctrl.Rule(distance_to_position['medium'] & distance_to_ball['high'] & player_function['attack'], ofensive_position['normal'])

    rule19 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['defense'], ofensive_position['bad'])
    rule20 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['midfield'], ofensive_position['normal'])
    rule21 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['low'] & player_function['attack'], ofensive_position['normal'])

    rule22 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['defense'], ofensive_position['bad'])
    rule23 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['midfield'], ofensive_position['bad'])
    rule24 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['medium'] & player_function['attack'], ofensive_position['normal'])

    rule25 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['defense'], ofensive_position['bad'])
    rule26 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['midfield'], ofensive_position['bad'])
    rule27 = ctrl.Rule(distance_to_position['high'] & distance_to_ball['high'] & player_function['attack'], ofensive_position['bad'])

    ofensive_position_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, 
                                                 rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, 
                                                 rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
    ofensive_positioning = ctrl.ControlSystemSimulation(ofensive_position_ctrl)

    return ofensive_positioning
